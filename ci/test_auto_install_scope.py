"""Guard Vender's 29-module source boundary and implicit installation.

This is a manifest-level regression guard. Runtime installation tests are required too.
"""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_AUTO = {
    "iap", "iap_mail", "sms", "mail_tracking_sms", "mail_bot", "resource_mail",
}
CORE_MODULES = set("""base web rpc bus auth_totp auth_passkey base_setup base_import base_import_module
base_report_wkhtmltox html_editor web_tour auth_password_policy auth_timeout
base_automation certificate http_routing mail privacy_lookup auth_oauth auth_signup
auth_totp_mail auth_password_policy_signup auth_ldap base_sparse_field
mail_tracking phone_validation resource web_hierarchy""".split())
NEEDED_AUTH = {"auth_passkey", "auth_totp", "auth_signup", "auth_totp_mail"}


def manifests():
    result = {}
    for addons_dir in (ROOT / "odoo" / "addons", ROOT / "addons"):
        for path in addons_dir.glob("*/__manifest__.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            body = next(
                item.value for item in tree.body
                if isinstance(item, ast.Expr) and isinstance(item.value, ast.Dict)
            )
            value = ast.literal_eval(body)
            result[path.parent.name] = value
    return result


def dependency_closure(packages, names):
    pending = list(names)
    selected = set()
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        selected.add(name)
        pending.extend(packages[name].get("depends", []) or (["base"] if name != "base" else []))
    return selected


def simulated_auto_install(packages, initial):
    selected = dependency_closure(packages, initial)
    while True:
        ready = set()
        for name, manifest in packages.items():
            if name in selected or manifest.get("installable", True) is False:
                continue
            auto = manifest.get("auto_install", False)
            if auto is False:
                continue
            dependencies = set(manifest.get("depends", []) or (["base"] if name != "base" else []))
            triggers = dependencies if auto is True else set(auto)
            if triggers <= selected:
                ready.add(name)
        if not ready:
            return selected
        new_selected = dependency_closure(packages, selected | ready)
        if new_selected == selected:
            return selected
        selected = new_selected


class TechnicalCoreAutoInstallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packages = manifests()
        if "web" not in cls.packages or "base" not in cls.packages:
            raise AssertionError("Incomplete Odoo checkout")

    def test_exact_29_modules_in_source(self):
        self.assertEqual(len(CORE_MODULES), 29)
        self.assertEqual(set(self.packages), CORE_MODULES)
        for name in EXCLUDED_AUTO | {"portal", "digest", "sms", "iap"}:
            with self.subTest(addon=name):
                self.assertNotIn(name, self.packages)
        for name, addon in self.packages.items():
            with self.subTest(addon=name):
                self.assertTrue(set(addon.get("depends", [])) <= CORE_MODULES)

    def test_core_and_mail_do_not_pull_excluded_addons(self):
        for roots in (("base", "web"), ("mail",), ("mail", "resource")):
            with self.subTest(roots=roots):
                installed = simulated_auto_install(self.packages, roots)
                self.assertFalse(installed & EXCLUDED_AUTO, installed & EXCLUDED_AUTO)
                self.assertFalse(installed & {"portal", "digest"}, installed & {"portal", "digest"})
                if "mail" in roots:
                    self.assertTrue(NEEDED_AUTH <= installed, NEEDED_AUTH - installed)


    def test_automation_rules_do_not_require_digest_or_portal(self):
        addon = self.packages["base_automation"]
        self.assertEqual(set(addon["depends"]), {"base", "mail", "resource"})
        self.assertNotIn("data/digest_data.xml", addon["data"])
        installed = simulated_auto_install(self.packages, ("base_automation",))
        self.assertTrue({"base_automation", "mail", "resource"} <= installed)
        self.assertFalse(installed & {"digest", "portal"} | (installed & EXCLUDED_AUTO))
        self.assertTrue(NEEDED_AUTH <= installed)


if __name__ == "__main__":
    unittest.main()
