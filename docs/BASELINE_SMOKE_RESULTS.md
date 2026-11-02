# Odoo 20 complete-source baseline — isolated acceptance results

**Date:** 2026-10-31. **Status:** research smoke tests passed; NOT ready for production or dependent Vender business integration.

## Provenance

- Public source: `AmgadSenan/vender-odoo-base`, upstream fork of `odoo/odoo:20.0`.
- Actual Odoo Community source SHA recorded in the official `odoo_20.0.20261015_all.deb` release metadata: `49529f034a60e4e9838e08e0a5616e5f2f38c601`.
- Reference runtime: `odoo:20.0-20261015@sha256:3de556969ca7916fe7d1a7fa3be2a49307a147c5fa1491bc2c57dcb0b950bea5`.
- Details and matching file hashes: [BASELINE_SOURCE_PROVENANCE.md](BASELINE_SOURCE_PROVENANCE.md).

## Completed tests

| Type | GitHub Actions | Result | Scope |
|---|---|---|---|
| Candidate source-parity prototype | [41171237513](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41171237513) | **Passed**, superseded source candidate | Full Odoo source vs official OS/Python base; CLI imports and addon count |
| Package-recorded SHA source parity | [41171511126](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41171511126) | **Passed** | Verify embedded package source SHA; Odoo CLI and module imports |
| Package-recorded SHA + ephemeral database | [41171706728](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41171706728) | **Passed** | Initialize `base,web` on disposable PostgreSQL `17.11`, `--stop-after-init` |
| Independent Ubuntu research image | [41171915475](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41171915475) | **Passed** | Build complete source from `ubuntu:24.04` OS packages; Odoo CLI, addons, assert that `odoo.deb` is not installed |
| Independent Ubuntu research image + ephemeral database | [41172067098](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41172067098) | **Passed** | Independent image builds and initializes `base,web` on disposable PostgreSQL `17.11` |

| Independent Ubuntu + PDF/RTL executable smoke + ephemeral database | [41172885635](https://github.com/AmgadSenan/vender-odoo-base/actions/runs/41172885635) | **Passed** | Patched-Qt `wkhtmltopdf 0.12.6.1`, `rtlcss 4.3.0`, structurally valid one-page Arabic HTML-to-PDF, RTL CSS property flips, PostgreSQL `17.11` `base,web` initialization |

**Important limit:** This PDF test checks that an Arabic HTML page produces a readable PDF structure and that rtlcss flips CSS properties. It does **not** verify visual Arabic shaping or real Odoo report generation; those require image inspection and functional report tests. The source image uses matching versions of PDF/RTL tools but is not yet a production runtime.

The comparison and independent images were built solely inside GitHub-hosted runners. **No images were published to a registry, and no Vender production containers or databases were changed.**

## Two separate research images

1. **`ci/Dockerfile.source-parity`:** replaces all Odoo Python/app source in the official pinned binary image. Useful for isolating source-code behavior with the existing OS/Python runtime, but **not** an independent distribution.
2. **`ci/Dockerfile.standalone-research`:** starts with `ubuntu:24.04`, installs Python distribution dependencies, then copies the **complete** Odoo Community source tree. No Odoo Docker base or `odoo.deb` dependency. Successful build and base/web database initialization establish **basic standalone runtime feasibility**, not production readiness.

## Remaining acceptance gates

- Pin and audit immutable OS base digest and Python/system dependency versions, and check security/licensing implications.
- **PDF/RTL executables are installed and passed synthetic smoke tests**; visually inspect Arabic font shaping and test real Odoo QWeb reports, assets, headers/footers and RTL rendering.
- Run Vender add-on integration and representative business workflows on an **isolated copy** of a Vender database and filestore, with external side effects disabled.
- Test installed module upgrades and schema/data compatibility, permissions, assets, WebSocket/bus, restart and rollback. Current `base,web` initialization is **not** full functionality coverage.
- Review source and image size, reproducibility, dependency CVEs, and release-build provenance before publishing any immutable image.
- Only after accepting the complete baseline, begin first small business addon extraction cycle; do not remove source modules based on installed/dependency counts alone.

**No approval for merging this Draft PR, changing the default upstream-tracking branch, deploying production, or uninstalling modules is implied by these results.**
