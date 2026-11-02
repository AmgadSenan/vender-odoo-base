# Vender Odoo Base

Independent **technical Odoo 20 Community foundation** for Vender, built from source rather than from the Odoo binary image. Application and business functionality belongs to [vender-business](https://github.com/AmgadSenan/vender-business).

## Frozen first-phase scope

The checked-out source includes **exactly 29 technical Odoo addons** across `odoo/addons/` and `addons/`. It excludes all remaining business, portal, IAP, SMS and test-fixture addons from the current source tree. This is the agreed **initial** technical core, not an assertion of final architectural completeness. The history of exclusions stays in Git.

The manifest inventory and dependency boundary are enforced by `ci/test_auto_install_scope.py`. Excluded modules are not in the Docker build context's addon directories.

## Build anywhere with Docker

From the root of this repository:

```sh
python3 -m unittest discover -s ci -p 'test_*.py' -v
docker build -f ci/Dockerfile.core-rc \
  --build-arg SOURCE_REVISION="$(git rev-parse HEAD)" \
  -t vender/odoo-base:core-29 .
docker image inspect vender/odoo-base:core-29 --format '{{.Id}}'
```

Supply an external PostgreSQL database and its credentials through the private deployment configuration. Example, with a PostgreSQL server reachable as `db` on an internal Docker network:

```sh
docker run --rm --network YOUR_PRIVATE_NETWORK vender/odoo-base:core-29 \
  --db_host=db --db_port=5432 --db_user=YOUR_DB_USER \
  --db_password=YOUR_DB_PASSWORD --database=YOUR_TEST_DB \
  --init=base_automation --without-demo --stop-after-init --no-http
```

Then run the image as an Odoo service with the same database options and a persistent `/var/lib/odoo` volume. Publish the HTTP port **only** through a suitably secured reverse proxy. Do not run against an existing production database or reuse the disposable testing filestore.

See [RC build and verification notes](ci/README.core-rc.md).

## Run the core locally with Docker Compose

The supplied `compose.yaml` builds the **same 29-addon source** and creates a fresh PostgreSQL 17 instance with persistent volumes. This example binds HTTP **only to your own computer**; it is not a public production deployment.

```sh
cp core.env.example .env
# Set VENDER_DB_PASSWORD in .env to a long random value.
export SOURCE_REVISION="$(git rev-parse HEAD)"
docker compose build odoo
docker compose up -d db
docker compose --profile setup run --rm init
docker compose up -d odoo
docker compose ps
```

Open `http://127.0.0.1:18073/web/login` (or the port in `.env`). The default initialization installs `base_automation` and its dependencies; other retained authentication and technical addons remain available for explicit installation. Use `docker compose down` to stop the example **without deleting database volumes**. Do not run `down -v` unless you intentionally want to destroy test data.

The sample uses a password in a local `.env` file and command-line options, which can be seen in local Docker metadata. For internet-facing use, first move credentials to an appropriate secrets/configuration mechanism and apply network and security hardening.

## Status and provenance

Odoo 20 source and original licenses are retained, including the root `LICENSE`. The current scope is a first independently buildable baseline. Deployment hardening, full security assessment, deeper source refactoring, and additional business modules remain later tasks.
