# SDK 0.2 Release Workflow

GC-SDK.03 defines the package/release mechanics for the existing Python and npm
SDK surfaces. It does not define new SDK functionality and does not itself
publish a release.

## Version boundary

The Python and npm package metadata must carry the same SDK version. A release
tag has the form `sdk-v<version>` and must exactly match both package metadata
versions.

For the current SDK 0.2 release surface, the expected version is `0.2.0`.

`tests/release_acceptance.py` checks:

- Python `pyproject.toml` and npm `package.json` versions match.
- npm `package-lock.json` is checked by the npm release workflow.
- a supplied release version matches package metadata.
- a `sdk-v<version>` GitHub ref is syntactically valid and matches metadata.

## Release workflow

Both package publication workflows are triggered by an `sdk-v*` tag or can be
run manually with an explicit version input.

### Python

`.github/workflows/main.yml` performs, in order:

1. resolve the release version from the tag or manual input;
2. run release metadata acceptance;
3. run the complete Python test suite;
4. build sdist and wheel artifacts;
5. run `twine check` on the artifacts;
6. publish the verified artifacts to the configured PyPI environment.

The workflow uses GitHub Actions OIDC for the PyPI publisher and keeps the
publication job dependent on the successful build job.

### npm

`.github/workflows/publish-js.yml` performs, in order:

1. resolve the release version from the tag or manual input;
2. install the locked dependency tree;
3. run the complete npm test/build suite;
4. verify `package.json` and `package-lock.json` versions;
5. run `npm pack --dry-run`;
6. publish the package with npm provenance.

The existing npm token authentication remains unchanged; changing repository
credential configuration is outside this code-level maintenance task.

## Non-goals

GC-SDK.03 does not:

- publish SDK 0.2.0 automatically as part of this change;
- create a new package version;
- introduce a release manager or runtime authority layer;
- silently rewrite package versions;
- infer a release version from an unrelated branch or commit.

A release remains an explicit repository/release decision after the release
workflows and package artifacts have passed their gates.
