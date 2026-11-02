# Vender technical-core boundary and security audit — review 10

Status: **review only; no source removals approved**. Parent: `3bbb758dad7a9a3de61eca2f20e5cb8224fc6aad` (cycle 09), which holds 81 top-level addons plus 15 manifest-bearing core addons.

## Findings

1. **Keep Odoo technical dependency chain intact:** `web` depends on `base`; `bus` depends on `web`; `mail` depends on `base`, `base_setup`, `bus`, `web_tour` and `html_editor`; `portal` depends on `auth_signup`, `base_address_extended`, `html_editor`, `http_routing`, `mail`, `web`; `payment` depends on `onboarding` and `portal`.
2. **Security modules are not optional by filename.** Keep `auth_signup`, `auth_totp*`, `auth_passkey*` and current policy modules until isolated login, password reset, access controls and MFA regression checks pass. Their `auto_install` and security side effects require testing.
3. **Business data bridges:** `product` requires `mail` and `uom`, and is a direct Vender dependency. `analytic` is required for original accounting modules if they are later reintroduced. `contacts`, `portal` and `payment` remain mixed and should not be pruned without future Vender application ownership and end-to-end tests.
4. **Hardware and peripheral integration:** keep `printer`, `iot_drivers`, and `iot_webserial` pending actual POS/peripheral requirements, rather than deleting by absence of a current manifest dependent.
5. **Remaining test addons:** preserve test coverage until the technical-core suite is established. Business-level tests removed in earlier cleanup cycles need a separate test path.

## Verified Vender business dependency risk (current main manifests)

- `vender_security` directly depends on `sale_management`, `purchase`, `account`, and `product`.
- `vender_taxless` depends on `account`, `sale_management`, `purchase`, and `product`.
- `vender_sale_platform` depends on `sale_management`; `vender_purchase_platform` depends on `purchase`.
- `vender_taxless_l10n_sa` depends on `l10n_sa` and `l10n_gcc_invoice`.
- `vender_whatsapp` requires `web` and `bus`; `vender_web_branding` requires `base_setup`, `mail`, `portal`; `vender_web_routing` requires `http_routing`.

**Consequence:** the stripped technical base intentionally does **not** run all existing Vender business addons by itself. The required original Odoo business addon set, including transitive dependencies, must first be sourced from one pinned upstream SHA and assigned to `vender-business/odoo_addons/` with a single active module owner. Do not mount these addons into core-only acceptance tests.

## Acceptance gates

- [ ] Full-source static scan for dynamic `odoo.addons` imports, XML IDs, JS assets, hooks and `auto_install` beyond declared Manifest depends.
- [ ] Build disposable exact-source image using the already cached Ubuntu/Odoo dependency runtime, not a new Ubuntu/Python package download.
- [ ] Initialize an isolated ephemeral PostgreSQL database with `base,web` and selected technical modules; test HTTP, assets, bus and mail startup.
- [ ] Test login/logout, signup/reset and MFA flows before pruning any `auth_*` or portal module.
- [ ] Test core data invariants and permissions; do not connect to production or an existing database.
- [ ] Transfer selected commercial modules into `vender-business/odoo_addons/` from the same pinned upstream SHA, then verify no duplicate active technical module names and test application installation.

**No new addon deletion, merge, deployment or production-database change** is part of this review. Earlier manifest-only audits and the cached older-image smoke check do not prove this exact source branch is runtime-compatible.
