#!/usr/bin/env python3
"""Check module-qualified file= references in loadable Odoo XML data.

Runs on source files without importing Odoo or starting a database.
Checks XML listed under data in every addon manifest, not demo XML.
"""
import argparse
import ast
import json
from pathlib import Path
import re
import sys

FILE_ATTR = re.compile(r"""<field\b[^>]*\bfile\s*=\s*["']([^"']+)["']""", re.DOTALL)
PATH = re.compile(r"^([a-z][a-z0-9_]*)/([^\s?#]+)$")

def addon_dirs(root):
    for folder in [root / "odoo" / "addons", root / "addons"]:
        if folder.is_dir():
            for item in sorted(folder.iterdir()):
                if item.is_dir() and (item / "__manifest__.py").exists():
                    yield item

def audit(root):
    modules = {p.name:p for p in addon_dirs(root)}
    scanned_xml = 0
    checked = 0
    missing = []
    parse_errors = []
    for module, folder in sorted(modules.items()):
        try:
            source = ast.parse((folder / "__manifest__.py").read_text(encoding="utf8"))
            literal = next(n.value for n in source.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Dict))
            manifest = ast.literal_eval(literal)
        except (OSError,StopIteration,SyntaxError,ValueError,TypeError) as ex:
            parse_errors.append({"module":module,"error":str(ex)})
            continue
        for source_file in manifest.get("data",[]):
            if not isinstance(source_file,str) or not source_file.endswith(".xml"):
                continue
            path = folder / source_file
            if not path.is_file():
                missing.append({"owner":module,"source":source_file,"target":source_file,"reason":"manifest_data_missing"})
                continue
            scanned_xml += 1
            data = path.read_text(encoding="utf8")
            for match in FILE_ATTR.finditer(data):
                value = match.group(1)
                detail = PATH.match(value)
                if not detail:
                    continue
                target_module, rest = detail.groups()
                checked += 1
                target_dir = modules.get(target_module)
                if target_dir is None or not (target_dir / rest).is_file():
                    missing.append({
                        "owner":module,
                        "source":source_file,
                        "line":data.count("\n",0,match.start())+1,
                        "target":value,
                        "reason":"module_absent" if target_dir is None else "file_absent"
                    })
    return {
        "modules":len(modules),
        "xml_data_files_scanned":scanned_xml,
        "module_qualified_file_references":checked,
        "missing_count":len(missing),
        "missing":missing,
        "manifest_parse_errors":parse_errors,
        "scope":"Only XML files referenced by manifest.data and <field file> attributes."
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base-root",type=Path,default=Path("."))
    p.add_argument("--json",type=Path)
    p.add_argument("--fail-on-missing",action="store_true")
    args=p.parse_args()
    result=audit(args.base_root)
    if args.json:
        args.json.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({**result,"missing":result["missing"][:40]},ensure_ascii=False,indent=2))
    return 1 if result["manifest_parse_errors"] or args.fail_on_missing and result["missing"] else 0

if __name__=="__main__":
    sys.exit(main())
