# Vender Odoo Base — Architecture Decision (2026-10-31)

## Purpose

This repository is a **public fork** of the Odoo Community source code, based on the official `odoo/odoo` repository and its `20.0` branch.

Vender intends to preserve Odoo as a maintained technical framework while progressively owning and simplifying the business application layer. **The starting point is the complete Odoo source tree.** No Odoo modules are removed during initial source acquisition.

## Repository and branch responsibilities

- **Upstream `odoo/odoo:20.0`:** authoritative source and security/maintenance updates.
- **`AmgadSenan/vender-odoo-base:20.0`:** clean fork branch intended to track upstream without Vender-specific edits.
- **`vender/architecture`:** this architecture documentation, reviewed separately from upstream.
- **`vender/baseline-20261015-candidate`:** pinned, unmodified upstream research commit `25e862d803aed1ff1a7cf3bef73b7686b8ef9741`. **Candidate only; not proven equivalent to any distributed Odoo package, container, or production deployment.**
- **`vender-business`:** separate **private** repository holding Vender-authored business applications and, in later migration cycles, selected original Odoo business addons.

## Incremental extraction strategy

1. **Full baseline:** build and validate an experimental runtime using the **entire** Odoo source tree at an explicit, recorded Git SHA. Establish functional parity in isolated environments before any deletions.
2. **Separate business addons:** move chosen Odoo business addons into the private business repository in small, testable batches. Preserve module technical identities, stable data behavior, and needed dependencies initially; ensure each addon name resolves from only one source in the final runtime.
3. **Clean the technical base:** remove or refactor business logic from this repository when replacement and compatibility tests pass.
4. **Customize Vender applications:** iteratively replace, simplify, and redesign inherited Odoo business behavior and dependencies. Do not retain upstream code merely for historical compatibility where it adds no value.
5. **Repeat:** every batch has its own review, source provenance, functional tests, and rollback strategy.

**Current module dependencies and installed-module lists are compatibility evidence, not a design constraint defining the final technical base.** Removing source code from a future image is different from uninstalling an addon or migrating records from an existing database.

## Public/private boundary

- No Vender business source, customer information, private deployment configuration, credentials, internal environment data, or secrets may be committed to this public repository.
- Preserve upstream copyright notices, contributor attributions, license texts, and the license obligations applicable to any redistributed changes.
- Do not automatically deploy upstream changes to production. Review and test them first.

## Status

**Architecture documented; no Vender Odoo Base runtime has yet been approved for production.** Source provenance, exact compatibility with the previously used Odoo binary distribution, independent Docker image builds, and full acceptance tests are separate work items.
