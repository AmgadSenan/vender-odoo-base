# Full Odoo core OCI production image — preparation contract

> **Decision override (2026-11-04):** The [adopted production release decision](https://github.com/AmgadSenan/vender-odoo-base/blob/main/docs/decisions/production-image-build-and-release.md) supersedes this document's mandatory GHCR/off-host build instructions. The current default is a controlled GitHub-source **build on the existing production server via Vender Production MCP**, with cached core reuse and the same production image tested and activated. Registry publication is optional. The technical core Dockerfile and historical tests remain useful; this external-publish procedure must **not** be treated as a required release step.


This repository owns the **complete Odoo 20 Community source**. The production
base image must be built from a fixed Git commit, then used as the immutable
`FROM` base of the private `vender-business` image. It is **not** an independent
Odoo service in the deployed Compose stack.

## Baseline and image recipe

- Approved architecture: all 660 upstream Odoo addons remain in this public
  source repository, with no premature source removal.
- Build recipe: `ci/Dockerfile.core-full` (the same complete-source recipe
  already exercised in development). Its `SOURCE_REVISION` argument and OCI
  revision label must equal the **exact commit being built**.
- Destination: `ghcr.io/amgadsenan/vender-odoo-base` under a versioned,
  non-reused tag and a content digest `@sha256:...`.
- Production builds must specify `ODOO_UID` and `ODOO_GID` from the currently running Odoo container and filestore volume. Local development continues to use automatic user allocation by default. A mismatch can break attachment reads/writes; never change live volume ownership to make a candidate pass.
- Platform for the existing Lightsail deployment: `linux/amd64`, to be
  confirmed against the target host during release preparation.
- The core image has **no Vender-private business code, production secret, or
  Odoo filestore**. Neither a running Odoo instance nor a database operation
  belongs to this build stage.

## Build/publish

Build and publish via the **controlled script in `vender-business`**,
`production/build-fullcore-images.sh`, which checks clean source trees,
explicit Git revisions, immutable OCI digests, and the derived image linkage.
Docker Buildx and existing GHCR authentication are required on the build
computer. The script produces source/digest release evidence but **does not
touch the production server or approve a deployment**.

The existing `Dockerfile.core-full` retains its development usage. This
production workflow does not silently change the local development Compose
stack. Use the resulting core digest when building the derived Vender image,
not its mutable development tag.

## Outstanding release checks

A build/push is not production acceptance by itself. Confirm the exact source
revision, dependency provenance, functional runtime, security updates,
`wkhtmltopdf`/RTL compatibility, and the versioned Vender production image's
entrypoint and healthcheck. The production release broker must separately
handle data/filestore checkpointing, the old anonymous
`/mnt/extra-addons` volume, and safe DB migrations.

Never run `docker compose up` for this core image on the live Vender database.
