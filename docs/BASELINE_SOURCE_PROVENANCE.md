# Odoo 20.0.20261015 — source provenance for the experimental baseline

**Status:** Verified package metadata and sample blob hashes; full integration testing remains in progress. Not an approval for production.

## Reference binary container

`odoo:20.0-20261015@sha256:3de556969ca7916fe7d1a7fa3be2a49307a147c5fa1491bc2c57dcb0b950bea5`

The existing image reports:
- Python `3.12.3` and `Odoo Server 20.0-20261015`.
- Installed Debian package `odoo` version `20.0.20261015`.
- The packaged `/usr/lib/python3/dist-packages/odoo/release.py` includes the build-generated record:

```python
version += '-20261015'
repos_heads = {
    'odoo': '49529f034a60e4e9838e08e0a5616e5f2f38c601',
    'enterprise': 'e2514184443254911c5e241b973e8b8af3b56675',
    'design-themes': '55c319cdffa8958de4ec4073560581df121bfaaf',
}
```

**Interpretation:** `49529f034a60e4e9838e08e0a5616e5f2f38c601` is the Odoo **Community** repository revision recorded by the installed Odoo package. The two other upstream revisions identify separate components and are **not** Vender source dependencies to import into the public fork.

## Source check

The public fork has branch `vender/baseline-20261015-package-source` pointing to the exact recorded Community source commit. The following sample Git blob SHA-1 hashes were obtained independently from the reference image's installed files and the GitHub repository at that commit:

| Relative Odoo source file | Matching Git blob SHA-1 |
|---|---|
| `odoo/orm/models.py` | `2a4373ea872f2801fdfbf4036158822f156ba701` |
| `odoo/addons/base/__manifest__.py` | `9dd740e1ad0dd63661e635c5cc3af27fc3e392a2` |
| `addons/web/__manifest__.py` | `18fc5ce17bd98c2a54b5aeb8f9090a1428e0dd33` |
| `addons/sale/__manifest__.py` | `9cfca823f4c7ba6336ce19fa97a26faba665b4ab` |

The `odoo/release.py` file does **not** have the same Git blob hash because the Debian packaging process appends the distribution-specific version and `repos_heads` metadata. This is expected and must not be mistaken for a source mismatch.

The previously guessed research commit `25e862d803aed1ff1a7cf3bef73b7686b8ef9741` is **not** the package-recorded revision; do not use it as the reference for the `20261015` binary comparison.

## Baseline acceptance boundary

- The official `20.0` branch of the fork tracks `odoo/odoo`; do not overwrite it with arbitrary Vender edits during research.
- `.github/workflows/vender-source-parity.yml` checks out the precise package-recorded Community SHA, builds an experimental source image, compares CLI behavior and attempts a disposable PostgreSQL 17 base/web registry initialization.
- The parity image inherits the original Ubuntu/Python runtime from the official Odoo binary container. It is **not** the long-term independent image.
- `ci/Dockerfile.standalone-research` is a separate experiment that starts from Ubuntu and installs Python dependencies without the Odoo Debian package; it has not yet passed build/tests.
- A passing CLI smoke test or a few matching file hashes **cannot** prove bit-for-bit package identity, compatibility with Vender addons, report rendering, or production readiness.
- No production DB, credentials, deployment, or user business source is used in these tests.
