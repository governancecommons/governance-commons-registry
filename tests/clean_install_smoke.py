"""Cross-platform smoke test against the built wheel, never editable source."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
wheel = next((ROOT / "dist").glob("*.whl"), None)
if wheel is None:
    raise SystemExit("built wheel not found")

subprocess.run(
    [sys.executable, "-m", "pip", "install", "--force-reinstall", str(wheel)],
    check=True,
)

command = shutil.which("gc-validate")
if command is None:
    raise SystemExit("installed gc-validate console script not found on PATH")


def expect(code: int, *args: str) -> None:
    result = subprocess.run([command, *args], text=True, capture_output=True)
    if result.returncode != code:
        raise SystemExit(
            f"expected exit {code}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


fixtures = ROOT / "tests" / "fixtures"
expect(0, "--spec", "ons", "--output", "json", str(fixtures / "valid checks ünicode.json"))
expect(1, "--spec", "ons", str(fixtures / "invalid checks ünicode.json"))
expect(2, "--spec", "ons", str(fixtures / "missing file.json"))
