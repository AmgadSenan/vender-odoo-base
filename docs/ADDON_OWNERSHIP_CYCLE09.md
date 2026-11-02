# Cycle 09 — technical core ownership review and optional integrations

**Status: source-only draft. Do not merge, deploy, or update any database until exact-source acceptance gates pass.**

## Provenance

- Parent source: `vender/cleanup-optional-business-eighth-pass` at `27fab8cc42109f0622b0c4d9eb96ed7eef242eb2`.
- Cycle-09 deletion source commit: `517781830f663aec0816fb1504dde5783e12bdf2`.
- This branch was derived from the newer Odoo 20 upstream and does not exactly match the `49529f0` locally cached baseline image. The prior baseline smoke result is not acceptance evidence for this source.
- The original Odoo source and archived reference branches remain unchanged.

## Audit of previous cycle 08

- Exact cycle-08 HEAD has **115 valid addon manifests**: 100 under `addons/` and 15 under `odoo/addons/`.
- Post-deletion audit exited successfully with **0 missing declared depends, 0 duplicate addon names and 0 manifest parse errors**. This cleared the pending manifest audit from cycle 08.

## Scope of cycle 09

Removed **19 individually reviewed optional integrations** from `addons/`:

- **Cloud storage:** `cloud_storage`, `cloud_storage_azure`, `cloud_storage_google`, `cloud_storage_migration`.
- **Third-party account/email/calendar:** `google_account`, `google_gmail`, `google_calendar`, `microsoft_account`, `microsoft_calendar`, `microsoft_outlook`.
- **Optional web/location tools:** `google_address_autocomplete`, `google_recaptcha`, `web_unsplash`, `base_geolocalize`.
- **Optional administration/business tools:** `api_doc`, `attachment_indexation`, `data_recycle`, `mysubscription`, `social_media`.

Declared reverse dependency validation on the 115-manifest parent source: **0 blockers in retained modules, 0 unresolved dependencies, 0 core module removals, 0 explicitly protected module removals**. Five removed manifests declare `auto_install`: `api_doc`, `google_gmail`, `microsoft_outlook`, `mysubscription`, `web_unsplash`; actual runtime side-effects require later testing.

Git tree verification before committing: `addons/` **100 → 81** directory entries; **all 81 retained addon trees unchanged**; no changes to `odoo/` or other root trees. This does **not** verify Python/JS/XML dynamic references in remaining source.

## Ownership triage of the 81 remaining `addons/` directories

| Classification | Count | Next disposition |
| --- | ---: | --- |
| Essential technical-service shortlist | 9 | Retain through exact-source smoke and integration tests |
| Technical extensions under necessity review | 42 | Validate use cases; prune only with dependency and runtime evidence |
| Mixed/business-dependent modules needing ownership decisions | 21 | Do not move or remove based on name alone |
| Test modules remaining | 9 | Preserve pending core test suite design and coverage audit |

### Core technical service retained (9)

`base_setup`, `bus`, `html_editor`, `http_routing`, `mail`, `resource`, `uom`, `web`, `web_tour`

### Technical extension candidate pending necessity review (42)

`auth_ldap`, `auth_oauth`, `auth_passkey`, `auth_passkey_portal`, `auth_password_policy`, `auth_password_policy_portal`, `auth_password_policy_signup`, `auth_signup`, `auth_timeout`, `auth_totp`, `auth_totp_mail`, `auth_totp_portal`, `barcodes`, `barcodes_gs1_nomenclature`, `base_address_extended`, `base_automation`, `base_import`, `base_import_module`, `base_install_request`, `base_report_paper_muncher`, `base_report_wkhtmltox`, `base_sparse_field`, `certificate`, `html_builder`, `iot_drivers`, `iot_webserial`, `link_tracker`, `mail_bot`, `mail_group`, `mail_plugin`, `mail_tracking`, `mail_tracking_sms`, `phone_validation`, `populate`, `printer`, `privacy_lookup`, `resource_mail`, `rpc`, `sms`, `sms_twilio`, `utm`, `web_hierarchy`

### Mixed/business-dependent or optional pending ownership review (21)

`analytic`, `board`, `calendar`, `calendar_sms`, `contacts`, `digest`, `gamification`, `iap`, `iap_mail`, `im_livechat`, `onboarding`, `partner_autocomplete`, `payment`, `portal`, `portal_discuss`, `portal_rating`, `product`, `rating`, `spreadsheet`, `spreadsheet_dashboard`, `spreadsheet_dashboard_im_livechat`

### Test addon retained pending coverage review (9)

`test_base_automation`, `test_html_field_history`, `test_mail`, `test_mail_sms`, `test_populate`, `test_resource`, `test_spreadsheet`, `test_translation_mode`, `test_utm`

## Architectural boundaries

- **Keep for now:** technical runtime (`base` under `odoo/addons`, `web`, `bus`, `mail`, `html_editor`, `http_routing`, `base_setup`, `resource`, `uom`, `web_tour`), plus shared or mixed foundations (`product`, `analytic`, `payment`, `portal`, `contacts`) until integration decisions are verified.
- **Authentication and security modules:** postpone pruning `auth_*` and any underlying security feature until identity flows and access controls are tested; several protected mixed modules depend on these.
- **Hardware and printing modules:** postpone pruning `iot_drivers`, `iot_webserial` and `printer` until retail POS/peripheral requirements are confirmed.
- **Spreadsheet/dashboard, onboarding, digest, gamification and live chat:** require own dependency and functional reviews before further pruning. `spreadsheet_dashboard` depends on `spreadsheet`; `board` depends on the dashboard; live-chat and mail tests overlap.
- **Ownership of future optional technical integrations:** when required again, re-add them to the technical-base source from the pinned upstream SHA. Only commercial app modules should be moved to `vender-business/odoo_addons/`; native Vender apps stay in `vender-business/addons/`.
- **Single active owner invariant:** combined runtime addon paths must not contain duplicate technical module names. An archival branch or unchanged source history does not count as a second active owner.

## Gates before merging any of the stacked draft cleanups

1. Repeat the manifest/uniqueness audit on cycle-09 exact commit and pin results.
2. Check imports, hooks, asset bundles, XML IDs, and optional integrations not captured by manifest `depends`.
3. Assess test coverage: `test_main_flows` was removed in cycle 04 and the marketing-specific tests in cycle 08; preserve suitable technical tests and restore business integration tests later.
4. On an isolated disposable PostgreSQL DB, build and initialize `base,web` from the exact cleaned source, then test HTTP/assets/auth/mail/bus and QWeb/PDF/RTL as needed.
5. Before commercial module transfer/activation, ensure compatible upstream SHA across both repos and no active addon name collisions.
6. No production database migration or module uninstall is part of these source-cleanup PRs.

## Links

- Parent cleanup PR: https://github.com/AmgadSenan/vender-odoo-base/pull/9
- Business architecture tracking: https://github.com/AmgadSenan/vender-business/issues/143
- Previous ownership inventory: `docs/ADDON_OWNERSHIP_CYCLE08.md`
