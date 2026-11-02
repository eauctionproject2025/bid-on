# -*- coding: utf-8 -*-
"""Render Mermaid (.mmd) via mermaid-cli + Chrome, PlantUML (.puml) via plantuml.com."""
from __future__ import annotations

import shutil
import subprocess
import zlib
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / "diagrams"
SRC = ROOT / "source"
SVG = ROOT / "exports" / "svg"
PNG = ROOT / "exports" / "png"
CFG = ROOT / "puppeteer-config.json"
DB_ERD = ROOT.parent / "database" / "erd"


def encode_plantuml(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]

    def encode6bit(b: int) -> str:
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        if b == 0:
            return "-"
        if b == 1:
            return "_"
        return "?"

    def append3bytes(b1: int, b2: int, b3: int) -> str:
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return "".join(encode6bit(c) for c in (c1, c2, c3, c4))

    out = []
    for i in range(0, len(compressed), 3):
        if i + 2 < len(compressed):
            out.append(append3bytes(compressed[i], compressed[i + 1], compressed[i + 2]))
        elif i + 1 < len(compressed):
            out.append(append3bytes(compressed[i], compressed[i + 1], 0)[:3])
        else:
            out.append(append3bytes(compressed[i], 0, 0)[:2])
    return "".join(out)


def mmdc(infile: Path, outfile: Path, scale: int | None = None) -> None:
    cmd = [
        "npx.cmd",
        "--yes",
        "@mermaid-js/mermaid-cli@11.4.0",
        "-i",
        str(infile),
        "-o",
        str(outfile),
        "-p",
        str(CFG),
    ]
    if scale:
        cmd += ["-s", str(scale)]
    print("mmdc", outfile.name)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr or r.stdout or f"mmdc failed for {infile}")


def render_plantuml(infile: Path) -> None:
    text = infile.read_text(encoding="utf-8")
    enc = encode_plantuml(text)
    stem = infile.stem.replace(" ", "_")
    for fmt, folder in (("png", PNG), ("svg", SVG)):
        url = f"https://www.plantuml.com/plantuml/{fmt}/{enc}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 BidOnThesisRenderer"})
        data = urlopen(req, timeout=90).read()
        out = folder / f"{stem}.{fmt}"
        out.write_bytes(data)
        print("plantuml", out.name, len(data))


def main() -> None:
    SVG.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    for mmd in sorted(SRC.rglob("*.mmd")):
        rel = mmd.relative_to(SRC).with_suffix("")
        stem = rel.as_posix().replace("/", "_")
        mmdc(mmd, SVG / f"{stem}.svg")
        mmdc(mmd, PNG / f"{stem}.png", scale=2)
    # PlantUML: use-case only (class-domain uses Mermaid class-domain.mmd)
    use_case = SRC / "use-case.puml"
    if use_case.exists():
        try:
            render_plantuml(use_case)
        except Exception as exc:
            print("plantuml warning:", exc)
            # fallback: mermaid use-case.mmd if present
            alt = SRC / "use-case.mmd"
            if alt.exists():
                mmdc(alt, SVG / "use-case.svg")
                mmdc(alt, PNG / "use-case.png", scale=2)
    # sync database ERD exports
    DB_ERD.mkdir(parents=True, exist_ok=True)
    for name in ("erd_erd.png", "erd_erd.svg"):
        src = (PNG if name.endswith(".png") else SVG) / name
        if src.exists():
            dest = DB_ERD / ("database-erd.png" if name.endswith(".png") else "database-erd.svg")
            shutil.copy(src, dest)
            print("copied", dest)
    (PNG / "README.md").write_text(
        "PNG exports rendered with Mermaid CLI (Chrome) and PlantUML server.\n"
        "Re-run: python docs/final-report/render_all_diagrams.py\n",
        encoding="utf-8",
    )
    (SVG / "README.md").write_text(
        "SVG exports rendered with Mermaid CLI (Chrome) and PlantUML server.\n"
        "Re-run: python docs/final-report/render_all_diagrams.py\n",
        encoding="utf-8",
    )
    print("DONE")


if __name__ == "__main__":
    main()
