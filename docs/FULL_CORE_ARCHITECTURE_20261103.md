# Vender architecture — complete Odoo 20 source (3 November 2026)

**Decision adopted.** This supersedes the previous 29-addon technical core and the repeated extraction/cleanup model.

## Source ownership and build

- **Public `vender-odoo-base`:** contains the *complete* Odoo 20 source trees, including all upstream standard addons, based on source revision `1cf08cf159a01c3d040a061de3c138e943918ac4`. Maintain only source and the minimal standalone Docker build support.
- **Private `vender-business`:** maintains original Vender modules and extensions. A standard Odoo addon is relocated here **only after an explicit customization/ownership decision**, not merely because it was imported as part of the previous architecture.
- There are **zero approved transfers** in this initial baseline. Extending a standard model or view using `_inherit` usually does not require transferring its original addon.
- A future approved transfer retains the original source in upstream Git. The derived **Vender runtime image only** removes that original addon copy, so the effective `addons_path` contains exactly one instance of its technical name. Preserve dependencies and upstream provenance.
- No Odoo module is deleted from the core source merely because it is not currently installed, needed or customized.

## Acceptance and subsequent work

The full-source base image and derived Vender image passed local builds. The latter ran 87 installed Odoo modules from an isolated copy of production data, passed Registry and filestore checks, and completed desktop/mobile browser smoke inspection after upgrading legacy Vender UI modules in that **isolated test DB**.

This is **architecture acceptance**, not a claim of readiness for production deployment or completeness of every business function.

The existing `vender_web` UI modules and modular view migration remain **transitional**; Vender may later directly customize the upstream `web` addon after a separate ownership/design decision. The architecture does not permanently require the bridge modules.

Historical source-removal proposals, 29-addon tests, and Odoo addon imports into Vender are obsolete. Their Git history and previously published images should be preserved for traceability, but not reused for new development.

No Vender private source, customer records, secrets, database dumps, private configurations or production files may be added to this public repository. Retain upstream authorship and license notices.
