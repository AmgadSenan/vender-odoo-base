# Cycle 10 — optional dashboards and engagement cleanup

Status: **staged draft only; not approved for merge or deployment**.

## Parent and scope

Parent branch: `vender/remove-electronic-payment-engine` at `743af38cba7c9c85e3acd343ff6e489d39e7ee18`.

Source deletion commit: `70b4b25191307b463a84623d86b92d1d3b93cabf`.

Five independent, nonessential Odoo addon directories are removed:
- `board` — classic dashboard views.
- `spreadsheet_dashboard` — spreadsheet-based dashboards.
- `spreadsheet_dashboard_im_livechat` — live-chat/dashboard integration, with `auto_install` on live chat.
- `gamification` — achievement and badge mechanics.
- `calendar_sms` — optional calendar-to-SMS integration.

The 75 retained top-level addon directory Git tree hashes are unchanged; no `odoo/` framework files changed. The original source is available in pinned upstream Git history.

## Exclusions and caution

- `spreadsheet` and `test_spreadsheet` remain. Removing spreadsheet itself would drag its test addon into the dependency closure.
- `im_livechat` remains because the retained `mail`, `calendar`, `portal`, `resource`, `rating` and related addon manifests reference its optional JS/asset bundles. Removing it now merits a separate asset-owner audit; absence of a declared `depends` is not enough.
- `digest` remains: removing it would break declared dependencies in `base_automation`, `im_livechat` and `mail_plugin`.
- `auth_*`, `portal`, `bus`, `mail`, `web`, `product` and `analytic` remain intact.
- Broad source mentions of `board` in icon names, `gamification` in generic view tests, and `spreadsheet_dashboard` in the optional web clickbot mapping were observed; these are not treated as manifest dependencies or a runtime failure in themselves.

## Verification

- Exact Git tree audit: `addons/` **80 → 75**, precisely the five intended directories deleted, all 75 others byte-for-byte unchanged.
- Manifest audit on the checked-out exact new source: **90 manifests** (75 top-level + 15 `odoo/addons`); **zero** missing declared dependencies, duplicate module names and parse errors.
- XML module-file reference audit on the exact source: **410** manifest-loaded XML data files, **17** module-qualified file refs, **zero** missing references.
- Offline Docker build: `vender/odoo-base:cleanup10-exact-70b4b25`, derived from existing cached Odoo runtime and source checkout of the actual cycle-10 commit, no Docker pulls or dependency install.
- Isolated PostgreSQL 17.11 init: `base,web,mail,portal,product,analytic` **PASS (exit code 0)**. SQL verified `base,web,bus,mail,portal,product,analytic,auth_passkey,auth_signup,auth_totp` installed. `im_livechat` and `spreadsheet` remain discoverable but were not installed by this core smoke.
- An HTTP check on this exact cycle-10 image was not completed because the container-launch request was blocked by the connected-command safety controls; prior-cycle HTTP results must not be misrepresented as this commit's HTTP evidence.

## Acceptance still needed

- Authenticated login, MFA, permissions, mail/bus and assets tests on the exact final source.
- Review generic framework tests that mention removed gamification/dashboard module names.
- Reconcile all stacked Draft PRs; do not merge or deploy solely on source/initialization smoke.
- Before running full Vender business apps, transfer required Odoo sales/purchase/account and localization addons to the intended business repository with a single active module owner.

[Architectural tracking issue](https://github.com/AmgadSenan/vender-business/issues/143) · [parent payment decision](docs/ARCHITECTURE_ELECTRONIC_PAYMENT_DECISION.md).
