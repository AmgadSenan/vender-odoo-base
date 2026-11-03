# Vender Odoo Base — Complete Odoo 20 Community source

> **Production release strategy (adopted 2026-11-04):** [Build and release decision](docs/decisions/production-image-build-and-release.md). The existing production host builds or reuses the pinned core image through Vender Production MCP. GitHub Actions/GHCR are optional, not deployment prerequisites; older external-build/publish guidance is historical.

This public repository contains the **complete Odoo 20 Community source tree** for Vender. The full baseline is from upstream Odoo revision `1cf08cf159a01c3d040a061de3c138e943918ac4` (3 November 2026). Unlike the abandoned *core-29* experiment, no standard Odoo addons are removed or excluded from this repository solely because Vender does not currently use them.

The independent Docker runtime is built from this source; it does not install an official prebuilt Odoo image or Odoo Debian package. Vender-authored business addons live exclusively in the **private** `vender-business` repository.

## Addon ownership

- All **660** upstream Odoo addon manifests are present under `odoo/addons/` and `addons/`, with their upstream names intact.
- Vender's original addons remain in `vender-business/addons/`, outside this public repository.
- **No standard addon has been approved for transfer** to Vender yet. The earlier imported Odoo business addons were a superseded experiment, not an accepted ownership decision.
- A future approved source customization may transfer an entire standard addon to the private repository, but its original files **stay in this Git source tree**. Only the *derived Vender runtime image* excludes that original copy so each technical name has one effective owner on `addons_path`.
- Ordinary Odoo extension modules may continue to use `_inherit` without transferring an upstream addon.

## Build full-source development image

```sh
python3 -m unittest discover -s ci -p 'test_*.py' -v
docker build -f ci/Dockerfile.core-full \
  --build-arg SOURCE_REVISION="$(git rev-parse HEAD)" \
  -t vender/odoo-base:full-source-dev .
docker run --rm --network none --entrypoint odoo vender/odoo-base:full-source-dev --version
```

The example `compose.yaml` uses PostgreSQL 17 and the same image recipe for disposable **local development only**, with browser access bound to loopback (`127.0.0.1:18073`). Supply a private `.env` based on `core.env.example`, then run:

```sh
docker compose build odoo
docker compose up -d db
docker compose --profile setup run --rm init
docker compose up -d odoo
```

Do not reuse production databases or filestores. Avoid `docker compose down -v` when preserving test data. Secrets must stay outside Git and need hardening before any network-accessible deployment.

For provenance, build details, and acceptance boundaries see [full-source notes](ci/README.full-source.md). The Vender-derived image and isolated production-clone browser tests are managed separately in `vender-business/development/full-core/`.

## Transition history

The 29-addon technical-core cleanup architecture and its earlier issues, research images, and documentation are **superseded**. Historical records remain in Git and in `docs/` for audit purposes; they are not the current build, addon-selection, or deployment instructions.

This architecture change does **not** declare either image production-ready. Source maintenance, dependency locking, operational hardening, and additional business customization remain separate work.
