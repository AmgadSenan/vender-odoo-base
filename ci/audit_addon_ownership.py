#!/usr/bin/env python3
"""Read-only Odoo addon ownership and dependency audit (Python standard library).

Usage:
  python3 ci/audit_addon_ownership.py --base-root .
  python3 ci/audit_addon_ownership.py --base-root . --business-root ../vender-business
  python3 ci/audit_addon_ownership.py --base-root . --remove-prefix l10n_ --require-no-blockers
  python3 ci/audit_addon_ownership.py --base-root . --remove-module account --json report.json

Never evaluates manifests, deletes files, changes databases, or changes git branches.
"""
import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import sys

TECHNICAL = {
    "base", "web", "bus", "mail", "base_setup", "html_editor",
    "http_routing", "web_tour", "uom", "resource",
}
REVIEW = {
    "analytic", "product", "payment", "portal", "contacts", "onboarding",
    "digest", "auth_signup", "base_address_extended", "base_automation",
    "website", "iap", "barcodes", "rating", "web_hierarchy",
}
BUSINESS = {
    "account", "crm", "sale", "purchase", "stock", "point_of_sale",
    "mrp", "hr", "project", "fleet", "repair", "event",
    "website_sale", "mass_mailing", "survey", "loyalty",
}
BUSINESS_PREFIXES = (
    "l10n_", "account_", "sale_", "purchase_", "stock_", "pos_",
    "mrp_", "hr_", "project_", "crm_", "website_", "event_",
    "fleet_", "repair_", "mass_mailing_", "spreadsheet_dashboard_",
    "payment_", "loyalty_", "marketing_card_", "sms_",
)

def extract_deps(manifest):
    """Read only the 'depends' literal; do not evaluate untrusted manifest code."""
    try:
        tree = ast.parse(manifest.read_text(encoding="utf-8"))
        obj = next(n.value for n in tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Dict))
        for key, value in zip(obj.keys, obj.values):
            if isinstance(key, ast.Constant) and key.value == "depends":
                deps = ast.literal_eval(value)
                if not isinstance(deps, (list, tuple)) or not all(isinstance(d, str) for d in deps):
                    return [], "non-literal depends"
                return deps, None
        return ["base"], None  # Odoo implicit default dependency.
    except (OSError, SyntaxError, ValueError, TypeError, StopIteration) as exc:
        return [], str(exc)

def category(name, location):
    if location == "base-core":
        return "technical_core"
    if name in TECHNICAL:
        return "technical"
    if name in REVIEW:
        return "review"
    if name in BUSINESS or name.startswith(BUSINESS_PREFIXES):
        return "business_candidate"
    if name.startswith("test_") or name.endswith("_test"):
        return "test_candidate"
    return "review"

def scan(directory, location):
    records = []
    if not directory.is_dir():
        return records
    for path in sorted(directory.iterdir()):
        mf = path / "__manifest__.py"
        if not path.is_dir() or not mf.is_file():
            continue
        deps, problem = extract_deps(mf)
        records.append({
            "name": path.name,
            "location": location,
            "path": str(mf),
            "depends": deps,
            "category": category(path.name, location),
            "parse_error": problem,
        })
    return records

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-root", type=Path, default=Path("."))
    p.add_argument("--business-root", type=Path)
    p.add_argument("--remove-prefix", action="append", default=[], help="Candidate group, e.g. l10n_")
    p.add_argument("--remove-module", action="append", default=[], help="Candidate exact module name")
    p.add_argument("--require-no-blockers", action="store_true", help="Fail when candidate removal breaks dependencies")
    p.add_argument("--require-unique-owner", action="store_true", help="Fail when module exists in multiple runtime paths")
    p.add_argument("--json", type=Path, help="Write report (optional); no source edits")
    args = p.parse_args()

    # A sparse checkout can expose this script while omitting every addon.
    # Never report a misleading "zero dependencies" from such a source.
    required_manifests = (
        args.base_root / "odoo" / "addons" / "base" / "__manifest__.py",
        args.base_root / "addons" / "web" / "__manifest__.py",
    )
    if not all(manifest.is_file() for manifest in required_manifests):
        print(
            "ERROR: incomplete Odoo source checkout; both core base and "
            "web manifests must be present before auditing dependencies",
            file=sys.stderr,
        )
        return 2

    modules = (
        scan(args.base_root / "odoo" / "addons", "base-core")
        + scan(args.base_root / "addons", "base-extras")
    )
    if args.business_root:
        modules += scan(args.business_root / "odoo_addons", "business-odoo")
        modules += scan(args.business_root / "addons", "business-vender")

    names = {}
    for item in modules:
        names.setdefault(item["name"], []).append(item)
    duplicates = {name: [item["location"] for item in entries] for name, entries in names.items() if len(entries) > 1}
    by_name = {item["name"]: item for item in modules if item["location"].startswith("base")}
    candidates = {
        name for name, item in by_name.items()
        if name in args.remove_module or any(name.startswith(prefix) for prefix in args.remove_prefix)
    }
    protected = sorted(candidates & (TECHNICAL | {"base", "web"}))
    candidates -= set(protected)
    retained = set(by_name) - candidates

    blockers = []
    for name in sorted(retained):
        item = by_name[name]
        for dep in item["depends"]:
            if dep in candidates:
                blockers.append({"dependent": name, "removed_dependency": dep})
    unknown = sorted({
        dep for name in retained for dep in by_name[name]["depends"]
        if dep not in retained and dep not in candidates
    })
    parse_errors = [{"module": m["name"], "error": m["parse_error"]} for m in modules if m["parse_error"]]

    result = {
        "scanned": len(modules),
        "by_location": dict(sorted(Counter(m["location"] for m in modules).items())),
        "by_category": dict(sorted(Counter(m["category"] for m in modules).items())),
        "duplicates": duplicates,
        "proposed_removals": sorted(candidates),
        "protected_candidates_not_removed": protected,
        "removal_blockers": blockers,
        "unresolved_dependencies_in_retained": unknown,
        "manifest_parse_errors": parse_errors,
        "scope": "Source manifests only: does not prove runtime safety, dynamic imports, or database compatibility.",
    }
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    failed = (
        (args.require_no_blockers and (blockers or protected or unknown or parse_errors))
        or (args.require_unique_owner and duplicates)
    )
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
