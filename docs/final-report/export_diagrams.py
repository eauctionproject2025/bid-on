# -*- coding: utf-8 -*-
"""Export Mermaid sources to SVG/PNG via mermaid-cli (Windows-safe)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "diagrams"
SRC = ROOT / "source"
SVG = ROOT / "exports" / "svg"
PNG = ROOT / "exports" / "png"


def npx_cmd() -> list[str]:
    for name in ("npx.cmd", "npx"):
        p = shutil.which(name)
        if p:
            return [p]
    return ["npx.cmd"]


def main():
    SVG.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    files = list(SRC.rglob("*.mmd"))
    print(f"Found {len(files)} mermaid files")
    base = npx_cmd() + ["--yes", "@mermaid-js/mermaid-cli@11.4.0"]
    for mmd in files:
        rel = mmd.relative_to(SRC).with_suffix("")
        stem = rel.as_posix().replace("/", "_")
        for folder, ext in ((SVG, ".svg"), (PNG, ".png")):
            out = folder / f"{stem}{ext}"
            cmd = base + ["-i", str(mmd), "-o", str(out)]
            print("Export", out.name)
            r = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if r.returncode != 0:
                print("FAIL", out.name)
                print(r.stderr[-800:] if r.stderr else r.stdout[-800:])
            else:
                print("OK", out, "bytes", out.stat().st_size if out.exists() else 0)
    print("Done")


if __name__ == "__main__":
    main()
