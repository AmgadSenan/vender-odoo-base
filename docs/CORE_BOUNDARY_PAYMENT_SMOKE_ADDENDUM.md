# Cycle 10 follow-up — provider catalogue isolation and XML asset audit

**Source:** `vender-odoo-base` cycle-09 exact source `3bbb758dad7a9a3de61eca2f20e5cb8224fc6aad`. Tests used locally cached runtime dependencies and fresh, disposable PostgreSQL 17.11 databases on an isolated Docker network.

## Verified regression: XML file references

Added `ci/audit_core_xml_file_refs.py` to examine module-qualified `<field file="module/path">` references in XML files listed by each addon Manifest's `data` key. The scan of the **unpatched** cycle-09 source found:

- 96 manifest-bearing addons (81 top-level and 15 under `odoo/addons`).
- **453 loadable XML data files** scanned.
- **54 module-qualified file references** checked.
- **24 missing files**, all under `addons/payment/data/payment_provider_data.xml`, pointing to files in removed `payment_*` provider directories.
- **0 manifest parse errors**.

The strict command `python3 ci/audit_core_xml_file_refs.py --base-root . --fail-on-missing` returns **exit code 1** on the unpatched source, as intended.

This check is narrowly scoped: it does not validate XMLIDs, JS assets, Python imports, runtime hooks, binary file contents or optional `demo` XML.

## Test-only isolations (not repository fixes)

Both experimental overlays are installed **only in derived disposable Docker images**, with the original source checkout and the exact-source image unchanged:

1. `vender/odoo-base:cleaned-no-upsell-smoke`: excludes `data/ir_module_module.xml` from the **base manifest load list**, avoiding missing Enterprise upsell category XMLIDs. `--init=base,web` exits **0** on a fresh DB, and HTTP tests showed `GET /web/login` **200** with login form + CSRF field, and anonymous `GET /web` **303** to the login page.
2. `vender/odoo-base:cleaned-no-provider-data-smoke`: additionally excludes `data/payment_provider_data.xml` from the **payment manifest load list**. `--init=base,web,mail,portal,payment,product,analytic` exits **0** on a different fresh DB.

SQL verification of test 2 showed these 12 modules as `installed`: `analytic`, `auth_passkey`, `auth_signup`, `auth_totp`, `base`, `bus`, `mail`, `onboarding`, `payment`, `portal`, `product`, `web`.

Separately, with just overlay 1, `base,web,mail,portal,product,analytic` initialized successfully; inclusion of `payment` **failed** because of missing `payment_adyen/static/description/icon.png`.

**Important:** Test 2 proves the payment engine can initialize without the legacy catalogue XML; it does **not** prove the system can run actual transactions with any provider. Provider metadata, configuration, registry entries and images need an explicit owner and installation strategy before reconnecting a provider module.

## Design decision needed before source patches

- **Base Enterprise placeholder catalogue:** decide whether to remove obsolete Enterprise upsell placeholder records or replace only their missing category dependencies, with migration/regression considerations. The test-only omission is a diagnostic, not the final implementation.
- **Payment provider catalogue:** separate provider-specific records and icon resources from the shared `payment` technical foundation, and rehome required providers/seed data together in the future business integration layer. A blind source deletion or restoring icons alone would not settle lifecycle ownership.
- Add the new XML file-reference audit to a future CI gate, but only after the designed ownership changes make the gate pass.
- Test exact updated core source (without experimental overlays), login/logout and MFA, permissions, mail/bus and QWeb/reporting. Neither a 200 login page nor modules marked `installed` establishes complete security correctness.

**No production containers/databases, active Vender application modules, upstream-tracking branches or original Odoo source were modified by these experiments.**
