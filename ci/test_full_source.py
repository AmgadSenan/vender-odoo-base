"""Prevent reverting the complete Odoo 20 source baseline to a pruned core."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MUST_EXIST = {
    "base", "web", "sale", "purchase", "account", "product",
    "payment", "stock", "portal", "mail", "contacts", "website",
}


class FullSourceInventoryTests(unittest.TestCase):
    def test_full_source_and_unique_addon_names(self):
        paths = []
        for root in (ROOT / "odoo" / "addons", ROOT / "addons"):
            self.assertTrue(root.is_dir(), str(root))
            paths.extend(p for p in root.iterdir()
                         if p.is_dir() and (p / "__manifest__.py").is_file())
        names = [p.name for p in paths]
        self.assertGreaterEqual(len(names), 650, "Unexpectedly pruned Odoo source")
        self.assertEqual(len(names), len(set(names)), "Duplicate standard addon names")
        self.assertFalse(MUST_EXIST - set(names), "Missing standard Odoo addons")

    def test_full_source_dockerfile_keeps_both_addon_trees(self):
        dockerfile = (ROOT / "ci" / "Dockerfile.core-full").read_text()
        self.assertIn("COPY --chown=odoo:odoo odoo/ /opt/odoo/odoo/", dockerfile)
        self.assertIn("COPY --chown=odoo:odoo addons/ /opt/odoo/addons/", dockerfile)
        self.assertNotIn("COPY --from=core-29", dockerfile)


if __name__ == "__main__":
    unittest.main()
