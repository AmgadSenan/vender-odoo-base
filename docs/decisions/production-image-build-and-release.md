# Decision: Vender image build and production release workflow

**Status:** Adopted — 2026-11-04  
**Scope:** Current Vender deployment on the existing production host  
**Related:** [Vender Business decision](https://github.com/AmgadSenan/vender-business/blob/main/docs/decisions/production-image-build-and-release.md) · [Production MCP decision](https://github.com/AmgadSenan/vender-dev-mcp/blob/main/docs/decisions/production-image-build-and-release.md)

## Goal and mandatory outcomes

Deliver Vender changes quickly through the **existing Vender Production MCP** with minimal cost, few moving parts, and recoverable production data. GitHub is the authoritative source repository; the current default is to **build the final deployment images on the existing production host from specifically selected Git revisions**, not to upload large images over the operator's home connection.

The development environment remains responsible for editing source, running development builds and tests, and reviewing changes before they reach the release workflow. The production-host builder checks out the **approved source revision** and builds the production image with controlled Docker build inputs; it does not become a general-purpose development workstation.

**Identity rule:** The image built on production is tested **before** activation, then the **same local image ID** is activated, and tested again **after** activation. There is no rebuild between those steps. A development-built image and an independently production-built image are *not* assumed to be byte-for-byte identical merely because their Git revisions match.

## Ownership of this repository

- `vender-odoo-base` owns the complete Odoo 20 Community source, its declared upstream revision and the Docker recipe for the core image.
- Preserve all upstream Odoo addon sources unless a separately agreed source-ownership task changes the architecture. Do not copy private business code, user secrets, databases or filestore contents into the core image.
- The core image becomes the base of the Vender image. **It is not a separate Odoo service** in production; the final `vender-business` image supplies the single Odoo container.
- Rebuild the core image only when the effective core source, Docker recipe, dependencies, platform or other material build inputs change. Reuse the existing tested local core image otherwise. Record its image ID and the source/build-input fingerprint; a mutable tag alone is not proof of identity.
- Changes to core source ownership (such as `web`) have their own explicit decision and acceptance tests; they do not become automatic side effects of an image release.

## Default release process

1. The developer finishes source changes, local builds/tests and code review; the intended core commit is recorded in GitHub.
2. Vender Production MCP fetches that **specific Git revision** into a controlled, temporary build workspace on the production host. It must not execute arbitrary source-supplied host scripts with production credentials.
3. If the core build inputs are unchanged, reuse the already validated local core image. Otherwise build a new core candidate using Docker's existing layer cache, with controlled resource usage so the running Odoo/database remain available.
4. Validate the resulting core image's source identity, target platform, Odoo runtime UID/GID, addon paths, startup basics and test results. Save the image ID/build record.
5. Pass that exact local core image identity to the derived Vender image build in `vender-business`; only the final derived image is activated in production.

No automatic build or deployment follows a Git push. GitHub Actions and GHCR **are optional tools**, not required steps, cost commitments or prerequisites of this workflow. If later measurements show that on-host builds materially disrupt production, revisit an external builder using actual time/cost/resource evidence, without changing the approved image-identity rule.

## Operational boundaries

- The actual Odoo filestore's numeric owner must be verified through MCP before choosing build UID/GID; never infer it solely from a development image.
- Do not stop or replace PostgreSQL, Caddy or their volumes when releasing the Odoo application image.
- Avoid new permanent staging infrastructure and recurring service fees unless a demonstrated operational need justifies them.
- Recovery of database and filestore, safe addon paths and controlled image rollback are required when a release can affect production data. Do not add redundant approval layers or unrelated security workflows as release prerequisites.

## Current implementation versus adopted decision

The full-source core Dockerfile and source architecture remain useful. The GHCR-specific publishing documentation/scripts proposed in [core PR #2](https://github.com/AmgadSenan/vender-odoo-base/pull/2) and [business PR #157](https://github.com/AmgadSenan/vender-business/pull/157) describe an **earlier, superseded default**; they are not the current release procedure. Their source changes may be reused after alignment, but no image registry, CI workflow or image upload is mandatory.

**This document governs future work when earlier build/publish instructions conflict.** Historical evidence may be retained, but must be labeled historical. Do not claim this decision is already implemented in the MCP.

**Acceptance for this repository:** Core images can be built or reused through MCP from pinned Git revisions, with an inspectable image ID, recorded inputs and a tested handoff to the final Vender image—without GHCR or the operator's device transferring image layers.
