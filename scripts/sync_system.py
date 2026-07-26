#!/usr/bin/env python3
"""Mirror one system's box art from libretro-thumbnails, re-encoded to WebP.

Usage: sync_system.py <System_Directory_Name>

Does a blobless sparse clone of the upstream repository (only Named_Boxarts/
is materialized), converts every image to WebP with the longest side capped at
MAX_SIZE, and replaces <System_Directory_Name>/ in the current working tree
with the fresh set. The caller (the workflow) commits the result.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

UPSTREAM = "https://github.com/libretro-thumbnails/{system}.git"
BOXARTS = "Named_Boxarts"
MAX_SIZE = 512
WEBP_QUALITY = 80


def clone_boxarts(system, workdir):
    repo = Path(workdir) / "upstream"
    subprocess.run(
        [
            "git", "clone", "--depth", "1", "--filter=blob:none",
            "--sparse", "--quiet", UPSTREAM.format(system=system), str(repo),
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "sparse-checkout", "set", BOXARTS],
        check=True,
    )
    return repo / BOXARTS


def convert(source_dir, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    converted = failed = 0
    for source in sorted(source_dir.iterdir()):
        if source.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        target = target_dir / (source.stem + ".webp")
        try:
            with Image.open(source) as image:
                # Palette images may carry transparency in tRNS, which only
                # survives an explicit RGBA conversion.
                wants_alpha = image.mode == "P" or "A" in image.getbands()
                image = image.convert("RGBA" if wants_alpha else "RGB")
                image.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)
                image.save(target, "WEBP", quality=WEBP_QUALITY, method=4)
            converted += 1
        except Exception as exc:  # a corrupt upstream file must not kill the sync
            print(f"skip {source.name}: {exc}", file=sys.stderr)
            failed += 1
    return converted, failed


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    system = sys.argv[1]
    output = Path.cwd() / system

    with tempfile.TemporaryDirectory() as workdir:
        boxarts = clone_boxarts(system, workdir)
        if not boxarts.is_dir():
            sys.exit(f"{system}: upstream has no {BOXARTS}/")
        staging = Path(workdir) / "converted"
        converted, failed = convert(boxarts, staging)
        if converted == 0:
            sys.exit(f"{system}: nothing converted (failed={failed})")
        # Replace, not merge: upstream renames/deletions must propagate.
        if output.is_dir():
            shutil.rmtree(output)
        shutil.move(str(staging), str(output))

    print(f"{system}: converted={converted} failed={failed}")


if __name__ == "__main__":
    main()
