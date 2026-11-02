# Cycle 08 — addon ownership inventory (provisional)

**Source:** `vender-odoo-base` cleanup cycle 07 commit `96633e8ebc87375248f9b370c54277f225afe678`.
**Decision:** remove the 40 commercial or optional business integrations in cycle 08; preserve all other addon trees for additional dependency and functional review.

**Classification is a triage aid, not proof of module role or permanent retention.** A module grouped as a technical extension may still be removed in a subsequent cycle; a mixed module may ultimately belong to the technical base or the business repository.
Classification covers the 140 top-level `addons/` directories at cycle 07. The framework `odoo/addons/` is separately owned by the technical base, and is not included in this count.

## Classification

| Classification | Directories | Status |
| --- | ---: | --- |
| Commercial or optional business extracted | 40 | Removed in cycle 08 |
| Core technical service retained | 9 | Retained for targeted review |
| Technical extension candidate pending necessity review | 59 | Retained for targeted review |
| Mixed/business-dependent or optional pending ownership review | 23 | Retained for targeted review |
| Test addon retained pending coverage review | 9 | Retained for targeted review |

## Directory names by classification

### Commercial or optional business extracted (40)

`event`, `event_booth`, `event_sms`, `fleet`, `fleet_maintenance`, `lunch`, `mail_tracking_mass_mailing`, `maintenance`, `mass_mailing`, `mass_mailing_event`, `mass_mailing_event_sms`, `mass_mailing_sms`, `mass_mailing_themes`, `payment_adyen`, `payment_aps`, `payment_asiapay`, `payment_authorize`, `payment_buckaroo`, `payment_custom`, `payment_demo`, `payment_dpo`, `payment_ecpay`, `payment_flutterwave`, `payment_iyzico`, `payment_mercado_pago`, `payment_mollie`, `payment_nuvei`, `payment_paymob`, `payment_paypal`, `payment_payu`, `payment_razorpay`, `payment_redsys`, `payment_stripe`, `payment_toss_payments`, `payment_worldline`, `payment_xendit`, `snailmail`, `survey`, `test_mail_full`, `test_mass_mailing`

### Core technical service retained (9)

`base_setup`, `bus`, `html_editor`, `http_routing`, `mail`, `resource`, `uom`, `web`, `web_tour`

### Technical extension candidate pending necessity review (59)

`api_doc`, `attachment_indexation`, `auth_ldap`, `auth_oauth`, `auth_passkey`, `auth_passkey_portal`, `auth_password_policy`, `auth_password_policy_portal`, `auth_password_policy_signup`, `auth_signup`, `auth_timeout`, `auth_totp`, `auth_totp_mail`, `auth_totp_portal`, `barcodes`, `barcodes_gs1_nomenclature`, `base_address_extended`, `base_automation`, `base_geolocalize`, `base_import`, `base_import_module`, `base_install_request`, `base_report_paper_muncher`, `base_report_wkhtmltox`, `base_sparse_field`, `certificate`, `cloud_storage`, `cloud_storage_azure`, `cloud_storage_google`, `cloud_storage_migration`, `data_recycle`, `google_account`, `google_address_autocomplete`, `google_calendar`, `google_gmail`, `google_recaptcha`, `html_builder`, `iot_drivers`, `iot_webserial`, `link_tracker`, `mail_bot`, `mail_group`, `mail_plugin`, `mail_tracking`, `mail_tracking_sms`, `microsoft_account`, `microsoft_calendar`, `microsoft_outlook`, `phone_validation`, `populate`, `printer`, `privacy_lookup`, `resource_mail`, `rpc`, `sms`, `sms_twilio`, `utm`, `web_hierarchy`, `web_unsplash`

### Mixed/business-dependent or optional pending ownership review (23)

`analytic`, `board`, `calendar`, `calendar_sms`, `contacts`, `digest`, `gamification`, `iap`, `iap_mail`, `im_livechat`, `mysubscription`, `onboarding`, `partner_autocomplete`, `payment`, `portal`, `portal_discuss`, `portal_rating`, `product`, `rating`, `social_media`, `spreadsheet`, `spreadsheet_dashboard`, `spreadsheet_dashboard_im_livechat`

### Test addon retained pending coverage review (9)

`test_base_automation`, `test_html_field_history`, `test_mail`, `test_mail_sms`, `test_populate`, `test_resource`, `test_spreadsheet`, `test_translation_mode`, `test_utm`

## Safety constraints

- The cycle-08 removal set includes 23 `payment_*` provider modules, but intentionally **retains the shared `payment` technical API**.
- Account, POS, sales/purchase/inventory, HR/projects and localization addons were extracted in earlier draft cycles; no commercial module has yet been transferred to `vender-business/odoo_addons/`.
- All removed module source remains retrievable at the pinned Odoo upstream reference; the `20.0` tracking branch is not modified.
- Dependency audits are **manifest-level only**. Python imports, data/XML references, JS assets, auto-install behavior and installed-database state are **not** verified by this classification.
- Removed tests `test_mail_full` and `test_mass_mailing` require later review of business and marketing test coverage; other test addons are retained provisionally.
- Before any merged runtime, all active addon paths across the two Vender repositories must contain **one module owner per technical name**.
- The source-cleanup branch is not authorized for production or database upgrades until an exact-source isolated acceptance test passes.

## Source provenance and related PRs

- Source baseline of this cycle: `96633e8ebc87375248f9b370c54277f225afe678`.
- Cycle-08 deletion commit: `6db7a2cf00ce82fc77e3f4a60209176c7aa58b28`.
- Source deletion count: 40 top-level addon directory entries, leaving 100.
- Parent cycle-07 PR: https://github.com/AmgadSenan/vender-odoo-base/pull/8
- Business architecture issue: https://github.com/AmgadSenan/vender-business/issues/143
