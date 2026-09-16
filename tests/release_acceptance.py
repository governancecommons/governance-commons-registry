"""Release acceptance checks for the dual Python/npm SDK surface.

The checks are intentionally local and side-effect free. Publication remains a
separate release action; this module verifies that a release tag cannot point at
mismatched package metadata.
"""

from __future__ import annotations

import json
import os
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_versions() -> tuple[str, str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    return pyproject["project"]["version"], package["version"]


def main() -> None:
    python_version, npm_version = _read_versions()
    if python_version != npm_version:
        raise SystemExit(
            f"package version mismatch: Python={python_version}, npm={npm_version}"
        )

    expected_version = os.environ.get("SDK_VERSION")
    if expected_version and python_version != expected_version:
        raise SystemExit(
            f"release version mismatch: metadata={python_version}, expected={expected_version}"
        )

    ref_type = os.environ.get("GITHUB_REF_TYPE")
    ref_name = os.environ.get("GITHUB_REF_NAME")
    if ref_type == "tag":
        if not ref_name:
            raise SystemExit("release tag ref is missing")
        match = re.fullmatch(
            r"sdk-v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", ref_name
        )
        if not match:
            raise SystemExit(f"invalid SDK release tag: {ref_name}")
        tag_version = ref_name.removeprefix("sdk-v")
        if tag_version != python_version:
            raise SystemExit(
                f"release tag mismatch: tag={tag_version}, metadata={python_version}"
            )

    print(f"release acceptance passed: SDK {python_version}")


if __name__ == "__main__":
    main()
