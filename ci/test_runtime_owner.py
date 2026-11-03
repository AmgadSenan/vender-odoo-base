"""Prevent source-image releases from changing the persistent filestore UID silently."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "ci" / "Dockerfile.core-full"


class RuntimeOwnerTests(unittest.TestCase):
    def test_production_can_pin_odoo_uid_and_gid(self):
        src = DOCKERFILE.read_text(encoding="utf-8")
        for text in (
            "ARG ODOO_UID=auto",
            "ARG ODOO_GID=auto",
            'groupadd --system --gid "$ODOO_GID" odoo',
            'useradd --system --uid "$ODOO_UID" --gid "$ODOO_GID"',
            'chown -R odoo:odoo /var/lib/odoo /opt/odoo',
        ):
            self.assertIn(text, src)

    def test_default_development_user_creation_remains_available(self):
        src = DOCKERFILE.read_text(encoding="utf-8")
        self.assertIn('if [ "$ODOO_UID" = "auto" ] && [ "$ODOO_GID" = "auto" ]', src)
        self.assertIn('useradd --system --create-home --home-dir /var/lib/odoo', src)


if __name__ == "__main__":
    unittest.main()
