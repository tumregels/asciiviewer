#!/usr/bin/env python3
"""
wxPython ships no PyPI wheel for Linux; it publishes prebuilt wheels per-distro at
https://extras.wxpython.org/wxPython4/extras/linux/gtk3/. pyproject.toml pins that
index to ubuntu-24.04 (what CI runs on) so the committed uv.lock stays reproducible.
On any other distro, run this instead of `uv sync` to install wxPython from the
matching per-distro wheel directory, without touching pyproject.toml/uv.lock.
"""
import platform
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

BASE_URL = "https://extras.wxpython.org/wxPython4/extras/linux/gtk3"
REPO_ROOT = Path(__file__).resolve().parent.parent


def detect_slug():
    info = platform.freedesktop_os_release()
    return f"{info['ID']}-{info['VERSION_ID']}"


def check_index(index_url):
    try:
        urllib.request.urlopen(urllib.request.Request(index_url, method="HEAD"))
        return True
    except urllib.error.URLError:
        return False


def wxpython_spec():
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        deps = tomllib.load(f)["project"]["dependencies"]
    return next(d for d in deps if d.lower().startswith("wxpython"))


def main():
    if platform.system() != "Linux":
        sys.exit("This script is for Linux only; run 'uv sync' directly on other platforms.")

    try:
        slug = detect_slug()
    except OSError:
        sys.exit("Cannot detect distro: /etc/os-release not found.")

    index_url = f"{BASE_URL}/{slug}/"
    if not check_index(index_url):
        sys.exit(f"No prebuilt wxPython wheels found for '{slug}' at {index_url}\n"
                 f"See {BASE_URL}/ for the list of supported distros.")

    spec = wxpython_spec()
    print(f"Detected {slug}; installing {spec} from {index_url}")

    subprocess.run(["uv", "sync", "--no-install-package", "wxpython"], cwd=REPO_ROOT, check=True)
    subprocess.run(
        ["uv", "pip", "install", "--python", str(REPO_ROOT / ".venv/bin/python"),
         "--find-links", index_url, spec],
        cwd=REPO_ROOT, check=True,
    )


if __name__ == "__main__":
    main()
