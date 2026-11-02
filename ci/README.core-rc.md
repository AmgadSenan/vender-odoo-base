# Vender Technical Core — First stable runtime candidate

This is a **release candidate for isolated testing**, the first agreed 29-addon source baseline; not yet a certified production image.

## Scope frozen for this candidate

- Based on the reviewed source after the IAP/Mail and `base_automation` decoupling changes.
- The current source tree and Docker image contain **exactly 29 approved-for-this-phase technical addons**. The other 57 were removed from the working tree in Git, with their history retained.
- IAP, SMS, portal, digest and optional mail bridges are absent from the checked-out source.
- The production runtime is source-based (does not use Odoo's official binary runtime).
- The image runs Odoo by default as an unprivileged user; no test credentials or DB data are baked in.

## Build

```sh
SOURCE_REVISION="$(git rev-parse HEAD)"
docker build -f ci/Dockerfile.core-rc \
  --build-arg "SOURCE_REVISION=$SOURCE_REVISION" \
  -t vender/odoo-base:core-29 .
docker image inspect vender/odoo-base:core-29 --format '{{.Id}}'
```

Retain the resulting image digest in release notes. The pinned Ubuntu base and upstream wkhtmltox/rtlcss versions reduce variation, but **apt packages are still updated by the distro**, and the build is not reproducibly locked.

## Test scope

Use a new, disposable PostgreSQL database and a private internal Docker network. Initialize `base,web` and `base_automation` separately. Verify login, Odoo uptime/healthcheck, module-source exclusion (IAP/SMS/portal/digest), automated-rule tests, and restart persistence.

Supply `--db_host`, `--db_user`, `--db_password`, and `--database` at runtime using private deployment configuration or secrets. Avoid exposing the test database or default administrator credentials publicly.

The release-candidate config lists only the retained technical addon directories. Consumers needing extra addons must explicitly configure their addon path when it is mounted and valid.

## Deferred, not ignored

Security review of public automation webhooks; integration UI and Arabic/RTL/PDF regression suites; OS/Python dependency locking and security scan; integration with vender-business; full live-deployment acceptance.

**Do not promote or publish as a production release solely on the basis of these smoke tests.**
