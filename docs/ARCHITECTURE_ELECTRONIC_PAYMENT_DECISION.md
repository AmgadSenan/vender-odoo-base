# Decision: exclude Odoo electronic payment gateways from Vender

**Status:** Approved architecture decision for the current Vender technical-core draft. Reintroduction requires a new explicit product and architecture decision.

**Decision date:** 2026-10-31.

## Scope

- Remove the entire `addons/payment` module from the cleaned technical-core source.
- The 23 `payment_*` provider addons were already removed in cleanup cycle 08. No electronic gateway/provider addon is retained in the currently proposed technical core.
- Preserve `portal`, `auth_*`, `onboarding`, `mail`, `bus`, `product` and `analytic`; no retained addon has a declared manifest dependency on `payment`.
- Do **not** transfer `payment` or payment-provider addons to `vender-business/odoo_addons` in the current business-module extraction phase.

## Rationale

The set of electronic payment providers integrated into Odoo does not currently satisfy Vender's operational needs in Yemen. Carrying their gateway engine, provider integrations, seed records and icon assets would introduce avoidable maintenance and runtime coupling without providing a needed feature.

## Important boundaries

- **Electronic payment gateways** and payment-provider integrations are excluded.
- **Accounting, invoicing, cash receipts, and manually recorded bank transfers** remain separate business concerns. Their implementation and future source ownership are not changed by this technical-core decision.
- `payment_custom` as an Odoo payment **provider** is excluded alongside other `payment_*` providers; this does not prohibit future business-side manual settlement features.
- The source is preserved in the original Odoo upstream reference and Git history. Restoration must be planned and tested, not assumed to be a one-line `depends` change.

## Exact source change and evidence

- Parent branch: `vender/fix-base-enterprise-catalogue` at `74db7144c35f639bce826d4bce5b9c0d2b1ce5a4`.
- Change commit: `00ea0d480b1ba4de81ac482d9b73f362dbd59729`.
- Delete exactly `addons/payment/` from the technical-core draft: **81 → 80** top-level addon directories; all 80 remaining directory Git tree SHAs unchanged.
- Manifest-level removal preflight found **zero reverse `depends` blockers**; no `odoo/addons` framework directory is affected.
- Previous payment-provider catalog repair in PR #13 is **superseded, closed unmerged**. Continue with the independent base-init patch PR #12.
- Test images / local source are research-only, not production releases.

## Acceptance and future review

1. Run exact-source manifest and XML-file reference audits after removal.
2. Run isolated fresh PostgreSQL core initialization and HTTP login smoke; do not mount `vender-business` addons until their unrelated sale/purchase/account dependencies have been transferred.
3. Preserve authentication, role/permission tests and explicit accounting data-flow tests before the final combined release.
4. A future need for online payment must specify locally available provider(s), integration mechanism, regulatory/security handling, and source ownership; then reintroduce and test the appropriate components only.

**No deployment, production database change, addon uninstall or existing-module migration is authorized by this draft source cleanup.**
