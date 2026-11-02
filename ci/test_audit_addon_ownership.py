"""Audit must fail closed on missing sparse-checkout addon roots."""
from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch


def load_audit():
    path = Path(__file__).with_name("audit_addon_ownership.py")
    spec = importlib.util.spec_from_file_location("odoo_audit_source_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditSourceCompletenessTests(unittest.TestCase):
    def setUp(self):
        self.audit = load_audit()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def invoke(self):
        out = io.StringIO()
        err = io.StringIO()
        with patch.object(sys, "argv", ["audit", "--base-root", str(self.root)]):
            with redirect_stdout(out), redirect_stderr(err):
                code = self.audit.main()
        return code, out.getvalue(), err.getvalue()

    def test_sparse_checkout_rejected_without_false_empty_success(self):
        (self.root / "ci").mkdir()
        (self.root / "docs").mkdir()
        code, out, err = self.invoke()
        self.assertEqual(code, 2)
        self.assertFalse(out)
        self.assertIn("incomplete Odoo source checkout", err)

    def test_missing_web_rejected_even_if_base_exists(self):
        manifest = self.root / "odoo/addons/base/__manifest__.py"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("{'name': 'Base'}\n", encoding="utf-8")
        code, out, err = self.invoke()
        self.assertEqual(code, 2)
        self.assertIn("web manifests", err)
        self.assertFalse(out)

    def test_full_minimal_source_can_still_audit(self):
        for name in ("odoo/addons/base", "addons/web"):
            path = self.root / name / "__manifest__.py"
            path.parent.mkdir(parents=True)
            path.write_text("{'name': 'Fixture', 'depends': []}\n", encoding="utf-8")
        code, out, err = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        result = json.loads(out)
        self.assertEqual(result["scanned"], 2)
        self.assertEqual(result["unresolved_dependencies_in_retained"], [])
        self.assertEqual(result["manifest_parse_errors"], [])


if __name__ == "__main__":
    unittest.main()
