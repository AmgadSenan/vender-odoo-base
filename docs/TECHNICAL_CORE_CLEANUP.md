# Vender technical-core ownership — first cleanup cycle

Status: **inventory/preparation only; no module deletions or runtime changes approved**.

## Purpose and source

- `vender-odoo-base`: Odoo technical framework and shared technical services.
- `vender-business/addons/`: Vender-authored business addons.
- `vender-business/odoo_addons/`: adapted original Odoo business addons.
- `odoo/odoo:20.0` / fork `20.0`: upstream source reference. Do not commit cleanup here.
- `vender/baseline-20261015-package-source`: pinned source matching the original 2026-10-15 image package metadata, SHA `49529f034a60e4e9838e08e0a5616e5f2f38c601`.
- This preparation branch was created from `vender/architecture`. **That branch follows a newer upstream source than the pinned image; its successful earlier smoke tests must not be transferred to this branch without rerunning them.** Choose and lock the integration/test SHA before pruning source.

The Odoo 20 fork `20.0` currently contains 645 addon directories in top-level `addons/`. These are not the same as the core `odoo/addons/` tree; do not remove or redesign `odoo/addons/base` in this phase.

## Initial ownership categories (provisional)

| Group | Examples | Target |
| --- | --- | --- |
| Framework core | `odoo/addons/base`, `web` | Technical base |
| Shared technical service | `mail`, `bus`, `html_editor`, `http_routing`, `base_setup`, `uom` | Technical base for initial runtime |
| Business application | `account`, `sale`, `purchase`, `stock`, `crm`, `point_of_sale`, `mrp`, `hr`, `project` and related `*_*` extensions | Business when needed, otherwise absent from runtime |
| Country-specific / localization | `l10n_*` (231 candidate directories in current top-level source count) | Business on demand; not core by default |
| Needs dependency/ownership decision | `product`, `analytic`, `payment`, `portal`, `contacts`, `onboarding`, `digest`, `auth_signup` | Do not remove solely based on name or current installed status |
| Test/auxiliary | `test_*`, `*_test`, `account_test` | Preserve test capability until replacement verification is in place |

This table is a grouping plan, **not** an audited complete ownership manifest.

## First deletion candidate — localization modules

`addons/l10n_*` is the initial batch proposed for review. Localization modules must **not** be removed until:
1. `ci/audit_addon_ownership.py --base-root . --remove-prefix l10n_ --require-no-blockers --json /tmp/odoo-addon-audit.json` finishes successfully on the chosen source tree.
2. The complete list of module names, manifests and dependency closure is inspected; a remaining module may not reference a deleted module through `depends`.
3. Dynamic import paths, data/XML references, `auto_install`, global hooks and module installation behavior are checked; the manifest script checks **only** declared `depends`.
4. Branch deletion commit includes the complete module list and upstream SHA; source can be restored verbatim from the original immutable ref.
5. The isolated technical-base build/registry/UI tests are re-run on the pruned branch. No production database or filestore is touched.

A failed blocker check is a **stop** signal; revise the batch, do not ignore the blocker.

## Explicit checks

Example inventory:

```bash
python3 ci/audit_addon_ownership.py --base-root . --json /tmp/odoo-addon-inventory.json
```

Example deletion proposal (read-only):

```bash
python3 ci/audit_addon_ownership.py --base-root . --remove-prefix l10n_ --require-no-blockers
```

Example uniqueness gate once both repositories are present:

```bash
python3 ci/audit_addon_ownership.py --base-root . --business-root ../vender-business --require-unique-owner
```

The branch, source archive, and clean upstream ref can contain archival duplicates. **Only the modules on active runtime addon paths must have a unique owner**, and the source/build inventory should match those active paths. `addons_path` must include the business repository's two addon directories only after their module names have been removed from the technical-base runtime source.

## Sequencing

1. Source inventory and declare ownership → review proposed first batch.
2. Create dedicated cleanup branch with approved source SHA and delete one consistent batch at a time → static dependency check.
3. Isolated technical-base build and smoke tests when new server access is ready.
4. Transfer original commercial addon directories (including full contents) from the **same pinned source SHA** to `vender-business/odoo_addons` as needed, without a second active source.
5. Run integration tests; then iteratively simplify/rebuild commercial addons in `vender-business` and core services in `vender-odoo-base`.

Related tracking: `vender-business` [#143](https://github.com/AmgadSenan/vender-business/issues/143) and [#145](https://github.com/AmgadSenan/vender-business/issues/145).