#!/usr/bin/env python3
"""Script to bump version numbers for the Marstek Venus E 3.0 integration.

Usage:
    python bump_version.py major  # 1.0.0 -> 2.0.0
    python bump_version.py minor  # 1.0.0 -> 1.1.0
    python bump_version.py patch  # 1.0.0 -> 1.0.1
    python bump_version.py 1.2.3  # Set specific version
"""

import argparse
import json
import re
from pathlib import Path


def get_current_version():
    """Get current version from manifest.json."""
    manifest_path = Path("custom_components/marstek_venus_e3/manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return manifest["version"]


def parse_version(version_string):
    """Parse version string into tuple of (major, minor, patch)."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_string)
    if not match:
        raise ValueError(f"Invalid version format: {version_string}")
    return tuple(map(int, match.groups()))


def bump_version(current_version, bump_type):
    """Bump version number based on type (major, minor, patch)."""
    major, minor, patch = parse_version(current_version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Assume it's a specific version string
        parse_version(bump_type)  # Validate format
        return bump_type


def update_manifest(new_version):
    """Update version in manifest.json."""
    manifest_path = Path("custom_components/marstek_venus_e3/manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["version"] = new_version

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Updated {manifest_path}")


def update_version_file(new_version):
    """Update VERSION file."""
    version_path = Path("VERSION")
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(new_version)

    print(f"Updated {version_path}")


def update_changelog(old_version, new_version):
    """Add placeholder for new version in CHANGELOG.md."""
    changelog_path = Path("CHANGELOG.md")

    with open(changelog_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert new version section after [Unreleased]
    from datetime import date
    today = date.today().isoformat()

    new_section = f"\n## [{new_version}] - {today}\n\n### Added\n\n### Changed\n\n### Fixed\n\n### Removed\n\n"

    # Find [Unreleased] section and insert after it
    unreleased_pattern = r"(## \[Unreleased\]\n)"
    content = re.sub(unreleased_pattern, r"\1" + new_section, content)

    # Update version comparison links at the bottom
    # Add new version link
    link_section_pattern = r"(\[Unreleased\]: .+?\.\.\.HEAD\n)"
    old_link = f"[Unreleased]: https://github.com/dnoshawork/MarstekHA/compare/v{new_version}...HEAD\n"
    new_link = f"[{new_version}]: https://github.com/dnoshawork/MarstekHA/compare/v{old_version}...v{new_version}\n"

    content = re.sub(link_section_pattern, old_link + new_link, content)

    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {changelog_path}")
    print(f"\nDon't forget to:")
    print(f"1. Edit CHANGELOG.md to add details about changes in version {new_version}")
    print(f"2. Commit the changes: git add -A && git commit -m 'Bump version to {new_version}'")
    print(f"3. Create a git tag: git tag -a v{new_version} -m 'Release v{new_version}'")
    print(f"4. Push changes: git push && git push --tags")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Bump version for Marstek Venus E 3.0 integration"
    )
    parser.add_argument(
        "version_arg",
        nargs="?",
        help="Type of version bump (major, minor, patch) or specific version (e.g., 1.2.3)",
    )

    args = parser.parse_args()

    # Determine what to bump to
    bump_arg = args.version_arg
    if not bump_arg:
        parser.print_help()
        return 1

    try:
        current_version = get_current_version()
        new_version = bump_version(current_version, bump_arg)

        print(f"Bumping version: {current_version} -> {new_version}")

        # Update all files
        update_manifest(new_version)
        update_version_file(new_version)
        update_changelog(current_version, new_version)

        print(f"\nVersion bump complete: {current_version} -> {new_version}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
