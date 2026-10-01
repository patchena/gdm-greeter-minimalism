# Release Process

## Version State

The release version must match in:

- `packaging/control`
- `packaging/changelog`
- `packaging/gdm-greeter-minimalism.1`
- `scripts/build-release.sh`
- `README.md`
- `docs/description.md`

The current version is `1.0.7`. The Debian changelog contains the release summary and timestamp from the local OS clock.

## Build and Verification

Build the package from the repository root:

```bash
./scripts/build-release.sh
```

Before publication:

- shell syntax and ShellCheck complete without errors
- `git diff --check` completes without errors
- package metadata reports the intended version and `Architecture: all`
- the command, extension runner, maintainer scripts, triggers, control metadata, conffile, autostart, README, target-state documentation, release procedure, changelog and manual page match their sources
- the Debian package installs successfully
- `gdm-greeter-minimalism verify` succeeds against the installed package
- the required manual Greeter validation succeeds

Fixes require a new installed package version before commit. Verify installed files against the inspected artifact, package integrity and the installed command. Installation and package maintenance do not restart GDM or end running sessions. Physical lock, VT-return, authenticated return and suspend/resume checks require the new Shell resources to be loaded in a user-coordinated session; source inspection and module parsing do not replace them.

## Commit and Tag

Validation installation uses only the conventionally built `.deb`. Source-tree execution or copied scripts do not substitute for package installation.

Before commit, review and update all project documentation. Stage with `git add -A`, commit the verified version content with a single-line version subject, push and verify the remote commit and clean worktree. Tags require separate authorization. An annotated tag uses the Debian version with a `v` prefix and points to the verified release commit. Published tags are never moved or reused.

## GitHub Release

GitHub publication requires separate authorization after all package and manual gates pass. The Release uses the immutable tag as its name and contains the matching versioned Debian package. It is complete only when published, not a draft or prerelease, linked to the tagged commit and exposing the inspected `.deb` as its binary asset.

## Verification

Verify remote branch and tag commit IDs, Release tag and target, draft/prerelease flags, asset name and downloaded asset checksum. Previous versioned release directories remain unchanged.
