# Cycle 12 — Odoo credit-paid services and Enterprise residue review

**Status: Draft, source cleanup only. Not approved for production, database migration or merging.**

## Scope and provenance

- Source parent: `vender/cleanup-optional-admin-eleventh-pass`, commit `5b0915bc369a7b83d9c3aba49d87faa2a3d817b3`.
- Core cleanup commit: `994e21eab7d969c4fb0cb157e7734ece0da56d3e`.
- Audited original 87 addon manifests (72 top-level, 15 under `odoo/addons`).
- The removed Odoo module `partner_autocomplete` was `iap_paid_service: True` and `auto_install: True`, matching official Odoo 20 partner-autocomplete documentation: each completed enrichment request consumes a paid IAP credit.
- The original Odoo 20 source is preserved in Git history; no files from proprietary Odoo Enterprise source repositories have been imported here.

## Removed and refactored

1. **Paid partner enrichment:** remove the entire `addons/partner_autocomplete` addon directory.
2. **Settings references:** remove `module_partner_autocomplete` from `addons/base_setup/models/res_config_settings.py` and its installation switch from `addons/base_setup/views/res_config_settings_views.xml`. Keep unrelated settings, including SMS, for later review.
3. **Dormant enrichment templates:** remove `addons/iap_mail/data/mail_templates.xml`, which defines only the no-longer-used enrichment templates; stop loading it in `iap_mail/__manifest__.py`. Remove its two dedicated SCSS stylesheets and asset entries. Retain the remaining `iap_mail` bridges needed by SMS until an explicit architectural decision.
4. **Enterprise upsell placeholder catalogue:** remove `odoo/addons/base/data/ir_module_module.xml` (already excluded from the base Manifest in PR #12) and all 23 files under `odoo/addons/base/static/img/icons/`, which an exact-source reference search found unused outside the removed catalogue. Update base Manifest comment to reflect physical removal.
5. Do **not** remove Odoo's legal/license headers, `ir.module.module` licence field and enum, generic module tooling, security modules, or upstream migration/lint code simply because they recognize Enterprise licence types. Such recognition is not the same as running licensed Enterprise applications.

## Integrity and test evidence

- Recursive Manifest reverse-dependency preflight for `partner_autocomplete`: **zero retained dependents**, no missing declared dependencies, no parse errors.
- Git tree on the parent versus the intended deletion commit: `addons/` **72 → 71** top-level directories; only `base_setup` and `iap_mail` retained addon trees changed, the other **69 retained addon trees byte-identical**. Within `odoo/addons/`, only the `base` tree changed. No unrelated root or framework module changes.
- Post-deletion `ci/audit_addon_ownership.py --require-no-blockers --require-unique-owner`: **PASS (exit 0)**, **86 manifests** (71 top-level, 15 core), **0** missing dependencies, duplicate module names or Manifest parse errors.
- XML module-file asset scanner: **PASS (exit 0)**, **399** Manifest-loaded XML data files, **17** module-qualified file references, **0** missing files.
- Offline Docker build from the actual checked-out deletion commit: `vender/odoo-base:cleanup12-paid-enterprise-994e21e`, using only a locally cached Ubuntu/Odoo runtime image.
- Isolated temporary PostgreSQL 17.11 fresh installation `base,web,mail,portal,product,analytic`: **PASS (exit 0)**. Database verified base/web/bus/mail/portal/product/analytic and the initial security modules installed, with `partner_autocomplete` absent.
- Database query of modules with `license='OEEL-1'` or `to_buy=True`: **0 Enterprise app-advertisement records**.
- One existing optional Markdown rendering dependency warning (`markdown2`) and an unused addons path warning from the cached runtime; neither was treated as evidence of a functional pass beyond this init smoke.

## Important outstanding Odoo IAP-credit dependency

Post-deletion manifests still contain:
- `iap` — `iap_paid_service=True`, `auto_install=True`.
- `sms` — `iap_paid_service=True`, `auto_install=True`.
- `iap_mail` — `auto_install=True` bridge, not itself flagged as a paid service.
- `mail_tracking_sms` — tracking integration for SMS.
- `sms_twilio` — optional Twilio external SMS adapter (third-party billing is a separate question).
- `base_automation` and corresponding tests, which depend directly or indirectly on the SMS stack.

**On the fresh test DB, `iap`, `iap_mail`, and `sms` still installed automatically.** This does not mean prepaid credits are consumed without a service call, but the Odoo-paid functionality remains available. Do not describe this cycle as complete removal of all credit-based integrations.

Recursive reverse-`depends` closure of removing `iap` totals **9 addon modules**, including `base_automation`, `test_base_automation`, and `test_mail_sms`. Deleting the entire closure would also remove general-purpose automation for reasons unrelated to paid usage. Next architectural decision: do we preserve `base_automation` by surgically decoupling Odoo's prepaid SMS backend, replace SMS with a locally suitable provider, or intentionally exclude automation in the initial product? No decision is implied here.

## Other Enterprise references

- Active addon Manifest audit: **zero** modules with `OEEL` or `OPL` licences.
- A few core code and test/migration references to `web_enterprise` or Enterprise licence values remain for general compatibility or testing. They are **not**, by themselves, Enterprise source modules, licence enforcement, subscription payments or paid app installations. They should be reviewed by use case, not blindly deleted.
- Old vendor licence notices and source attribution are retained.

## Acceptance gates

- Test installing/upgrading an existing disposable source-compatible database, especially `base_setup` settings and any legacy XMLID names.
- Test Settings UI, mail templates, authentication, assets, bus, and full core functional flows; this cycle covered static checks and fresh initialization only.
- Decide whether/how to decouple paid SMS/IAP from general automation before another removal batch.
- Keep all draft PRs unmerged and all existing databases/production untouched until consolidated source acceptance.

Official references:
- https://www.odoo.com/documentation/20.0/applications/sales/crm/optimize/partner_autocomplete.html
- https://www.odoo.com/documentation/20.0/applications/essentials/in_app_purchase.html
