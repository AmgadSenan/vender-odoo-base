# Cycle 11 — optional administration and mail plugin addon cleanup

**Status: staged Draft PR only. Not approved for merge or production rollout.**

## Provenance and scope

Parent cleanup: `vender/cleanup-optional-engagement-tenth-pass`, commit `7de4a50277ef4b8e6ebb00283ca7b43ed630d6a4`.
Deletion commit: `838ee6f5cffb72b16d73fe6ce76be2f207d7c38e`.

Exactly three optional addons extracted from `addons/`:
- `base_install_request`: Odoo application installation request workflow.
- `base_report_paper_muncher`: optional paper document digitization engine.
- `mail_plugin`: CRM/email plugin integration.

Manifest reverse dependency analysis found **zero retained dependents** for all three. Source scan of 7,091 Python, XML, JS, CSS, JSON and related files found no active cross-module references for `mail_plugin` or `base_report_paper_muncher`. The only detected reference to `base_install_request` was in a generic base framework test name collection.

## Conservative exclusions

Do **not** remove `base_import_module` in this cycle: `odoo/cli/deploy.py` explicitly uses its deployment upload endpoint. Odoo development and deployment strategy needs a separate decision before trimming it.

Do **not** remove `partner_autocomplete` in this cycle: `iap_mail/data/mail_templates.xml` references a static image file from it; removing the addon would create an asset dependency defect until the template is revised.

Keep all authentication modules, `web`, `mail`, `bus`, `portal`, `product`, `analytic`, hardware/printing integrations, `im_livechat` and generic framework/addon test suites.

## Verification

- Git tree: `addons/` **75 → 72 directories**; exactly the intended 3 removed; **all 72 retained directory tree hashes identical**; no `odoo/` or other root tree changes.
- Exact deletion commit Manifest audit: **87 manifests** (72 top-level, 15 framework); **0 missing declared dependencies, 0 duplicate module names, 0 parse errors**.
- Manifest-loaded XML file references audit: **404 XML data files**, **17 module-qualified file references**, **0 missing references**.
- Docker image built **offline**, without downloads or package installs, from exact source commit: `vender/odoo-base:cleanup11-exact-838ee6f` using the previously cached Ubuntu/Odoo runtime image.
- Isolated ephemeral PostgreSQL 17.11 fresh init `base,web,mail,portal,product,analytic`: **PASS, exit 0**. SQL verified `analytic`, `auth_passkey`, `auth_signup`, `auth_totp`, `base`, `bus`, `mail`, `portal`, `product`, `web`, and the deliberately retained `base_import_module` and `partner_autocomplete` as installed.
- Runtime warning: `markdown2` unavailable for mail Markdown rendering; unused `/mnt/extra-addons` addon path warning. Not treated as test failures, but runtime dependencies/config must be reviewed before production.
- HTTP, authenticated login, MFA, mail/bus and full Vender commercial addon integration are **not yet accepted or tested on this exact source**.

## Next release gates

1. Full module ownership and static code/asset inspection across remaining technical extensions.
2. End-to-end authentication and permission checks and actual `mail`/`bus` behavior.
3. Restore appropriate sales/purchase/account/localization addons from pinned original Odoo source to `vender-business/odoo_addons`, with one active owner per module before business integration acceptance.
4. Review deferred `base_import_module` CLI and `partner_autocomplete` IAP template references before any future removal.
5. Do not merge into main or alter any existing database until exact-source acceptance and explicit approval.

No production or existing data changes occurred.
