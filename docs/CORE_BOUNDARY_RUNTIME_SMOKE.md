# Vender technical-core exact-source runtime smoke — cycle 10 investigation

**Status:** Investigative, **not production ready**. No core source fix has been accepted or merged.

## Provenance and reuse

- Cleaned source SHA: `3bbb758dad7a9a3de61eca2f20e5cb8224fc6aad`, branch `vender/cleanup-external-integrations-ninth-pass`.
- Source was checked out into an isolated local WSL clone; full checkout includes `odoo/`, `addons/` and `odoo-bin`, totaling about 354 MB of files.
- The existing locally cached Ubuntu runtime image `ghcr.io/amgadsenan/vender-odoo-base:research-20261015-49529f0` supplied dependencies; **no Docker image pull, apt or pip installation** was required.
- Built exact-source image `vender/odoo-base:cleaned-exact-3bbb758` with `docker build --pull=false --network=none`. Source itself matches cycle-09 SHA; runtime dependencies come from the older reference image and are **not yet independently pinned for this source SHA**.
- Tests used `postgres:17.11-bookworm` already cached locally and separate disposable databases on an isolated Docker internal network with **no host port publishing**.

## Test outcomes

| Test | Result | Evidence / limitation |
| --- | --- | --- |
| Exact-source Docker image build | **PASS** | All 81 top-level addons copied from the source checkout, replacing the older source tree completely |
| `odoo --version` and Python import | **PASS** | Odoo Server 20.0; `import odoo, odoo.cli` |
| Source sanity | **PASS** | 81 top-level addons, original `odoo/addons/base` present; `sale`, `account` and `point_of_sale` absent |
| PDF/RTL executables | **PASS** | `wkhtmltopdf 0.12.6.1` with patched Qt and `rtlcss 4.3.0` are installed. No QWeb visual report test |
| Exact-source `--init=base,web` on disposable DB | **FAIL** | Missing XMLID `base.module_category_services_timesheets` referenced by `odoo/addons/base/data/ir_module_module.xml` |
| Test-only image excluding the above Enterprise upsell XML file from base's manifest | **PASS** | `vender/odoo-base:cleaned-no-upsell-smoke` initializes `base,web` on a **new** disposable DB, exits 0 |
| Database installed-state verification after test-only patch | **PASS** | `base`, `web`, `bus`, `auth_totp`, `auth_passkey` installed |
| Local unauthenticated HTTP smoke | **PASS** | `GET /web/login` returned 200, login form and CSRF token present; `GET /web` returned 303 redirect to `/web/login`. No host port published |
| `--init=base,web,mail,portal,product,analytic` after test-only patch | **PASS** | All requested modules and `auth_signup` verified installed in a separate disposable DB |
| `--init=base,web,mail,portal,payment,product,analytic` after test-only patch | **FAIL** | `payment/data/payment_provider_data.xml` references missing `payment_adyen/static/description/icon.png` |

Warnings seen on otherwise successful tests: unused `/mnt/extra-addons` not present; Python `markdown2` unavailable for Markdown rendering. These are not acceptance by themselves.

## Confirmed cross-module couplings not covered by Manifest `depends`

**A. Odoo Enterprise upsell stub categories:** Stock `odoo/addons/base/__manifest__.py` loads `data/ir_module_module.xml`, which contains placeholder records for additional Odoo Enterprise apps. Some `category_id` XMLIDs (e.g. `base.module_category_services_timesheets`) are absent from the pruned module catalog. The exact-source core boot failed; a **test-only** omission of this file from the manifest made the basic boot succeed. This does not yet authorize removing that load line from the repository, because references/upgrade semantics and other enterprise placeholders need review.

**B. Odoo payment provider icon seeding:** `addons/payment/data/payment_provider_data.xml` contains 25 payment provider record definitions and references provider-specific image files under removed `payment_*` addon directories. When `payment` is installed, XML data loading fails on the missing Adyen icon. Keep `payment` technical API while designing a separation for optional provider records/assets. Moving provider addons back later will also need the correct seed records and compatible installation order.

**C. Static scan, candidate findings:** Across ~7,381 Python/XML/JS/CSS/SCSS/JSON/HTML/CSV files, a deliberately broad search flagged 753 possible references to absent addon names; most are false positives (e.g. XML placeholder names). High-confidence Python imports included `odoo/addons/test_l10n/tests/test_country.py` references to removed accounting tests and `addons/payment/models/res_country.py` references to removed Stripe/Mercado Pago code. The latter imports are guarded by `try/except ModuleNotFoundError`, so an import reference alone is not evidence of failure. These candidates are **not** a validated list of 753 defects.

## Cross-repository integration constraints (vender-business main manifests)

- `vender_security`: `sale_management`, `purchase`, `account`, `product`.
- `vender_taxless`: `account`, `sale_management`, `purchase`, `product`.
- `vender_sale_platform`: `sale_management`.
- `vender_purchase_platform`: `purchase`.
- `vender_taxless_l10n_sa`: `l10n_sa`, `l10n_gcc_invoice`.
- `vender_whatsapp`: `web`, `bus`.
- `vender_web_branding`: `base_setup`, `mail`, `portal`.

These make it **incorrect** to use the cleaned core alone as a runtime for the existing full Vender business addon set before moving their Odoo commercial dependencies to `vender-business/odoo_addons/`. Core-only smoke tests must exclude these addons; later integrated tests must use one active owner per technical addon name.

## Next acceptance work / blockers

1. **Fix base boot coupling in a separate reviewed code patch**, preferably by carefully decoupling unused Enterprise upsell placeholder records from the technical core rather than reintroducing business addons solely to create categories. Re-run fresh `base,web` initialization without test-only overrides.
2. **Fix payment's provider data/asset coupling** in a separate patch; make provider seed records/assets follow chosen owner and installation stage. Re-run fresh `payment` integration.
3. Add a static audit for cross-addon `file=` references in XML and explicit missing Python imports, with manual false-positive review.
4. Test authenticated login, reset and MFA, bus/WebSocket, mail/portal permissions, QWeb/PDF/RTL and restart with an isolated database; current HTTP 200/303 smoke is **not** a security audit.
5. Test full Vender business installation only after transferring required source-matched addons and ensuring no runtime duplicates.

**No original source was modified for the two diagnostic runtime experiments; changes are confined to derived disposable test images. No production database, existing Docker volumes or deployment were touched.**
