# Release Process

## Version State

The release version must match in:

- `packaging/control`
- `packaging/changelog`
- `packaging/gdm-greeter-minimalism.1`
- `scripts/build-release.sh`
- `README.md`
- `docs/description.md`

The Debian changelog contains the release summary and final release timestamp.

## Build and Verification

Build the package from the repository root:

```bash
./scripts/build-release.sh
```

Before publication:

- shell syntax and ShellCheck complete without errors
- `git diff --check` completes without errors
- package metadata reports the intended version and `Architecture: all`
- the command, README, target-state documentation, changelog, and manual page in the package match their sources
- the Debian package installs successfully
- `gdm-greeter-minimalism verify` succeeds against the installed package
- the required manual Greeter validation succeeds

## Commit and Tag

The verified release content is committed and pushed before tagging. The annotated tag uses the Debian version with a `v` prefix and points to the exact release commit.

For version `1.0.4`:

```bash
git push origin main
git tag -a v1.0.4 -m "v1.0.4"
git push origin v1.0.4
```

Published tags are not moved or reused.

## GitHub Release

The GitHub Release uses the tag as its name and contains the matching Debian package as a binary asset.

For version `1.0.4`:

```bash
gh release create v1.0.4 \
  release/v1.0.4/gdm-greeter-minimalism_1.0.4_all.deb \
  --repo patchena/gdm-greeter-minimalism \
  --verify-tag \
  --title "v1.0.4" \
  --notes "Disable all Greeter system sounds."
```

The release is complete only when it is published, is not marked as a prerelease, targets the tagged commit, and exposes `gdm-greeter-minimalism_1.0.4_all.deb` as an asset.

## Verification

```bash
git ls-remote --tags origin refs/tags/v1.0.4
gh release view v1.0.4 \
  --repo patchena/gdm-greeter-minimalism \
  --json tagName,targetCommitish,isDraft,isPrerelease,assets,url
```
