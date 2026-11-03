# Full Odoo 20 source image — current development baseline

The complete upstream Odoo 20 addon trees (`odoo/addons` and `addons`) originate from commit `1cf08cf159a01c3d040a061de3c138e943918ac4`. Their contents were verified byte-for-byte against the upstream source tree before integration into this repository's existing `main` history. There are **660** distinct standard addon names.

`ci/Dockerfile.core-full` is the active, independent source-image recipe. It does not filter addon directories. `ci/Dockerfile.core-rc` and older research Dockerfiles, 29-module tests, or reports from earlier history are not the current build contract.

## Checks

```sh
python3 -m unittest discover -s ci -p 'test_*.py' -v
docker build -f ci/Dockerfile.core-full \
  --build-arg SOURCE_REVISION="$(git rev-parse HEAD)" \
  -t vender/odoo-base:full-source-dev .
docker run --rm --network none --entrypoint odoo vender/odoo-base:full-source-dev --version
```

The Vender image is a **separate build** from `vender-business` with its own module ownership guard. Under the initial architecture, the approved transfer list is empty; no upstream addon is removed from either Git source or the base image.

Source, image construction, cloned-database Registry, and actual browser checks have been performed for the baseline. They do not establish complete functional/security readiness or permission to deploy.

The public repository contains Odoo source and its independent build files only. Do not commit private addons, real database/filestore contents, access keys or any environment secrets.
