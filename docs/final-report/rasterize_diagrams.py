# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

SVG = Path(__file__).resolve().parents[1] / "diagrams" / "exports" / "svg"
PNG = Path(__file__).resolve().parents[1] / "diagrams" / "exports" / "png"
DB_ERD = Path(__file__).resolve().parents[1] / "database" / "erd"


def main():
    PNG.mkdir(parents=True, exist_ok=True)
    for svg in sorted(SVG.glob("*.svg")):
        text = svg.read_text(encoding="utf-8")
        titles = re.findall(r'font-weight="bold">([^<]+)', text)
        lines = re.findall(r'font-size="14">([^<]+)', text)
        title = titles[0] if titles else svg.stem
        img = Image.new("RGB", (1200, 675), "white")
        d = ImageDraw.Draw(img)
        d.rectangle([20, 20, 1180, 655], outline="black", width=2)
        y = 50
        d.text((40, y), title[:95], fill="black")
        y += 42
        for ln in lines:
            d.text((40, y), ln[:115], fill="#222222")
            y += 28
        d.text((40, 640), "Bid On thesis diagram export (fallback raster)", fill="#666666")
        out = PNG / f"{svg.stem}.png"
        img.save(out)
        print("wrote", out)
    erd = PNG / "erd_erd.png"
    if erd.exists():
        DB_ERD.mkdir(parents=True, exist_ok=True)
        shutil.copy(erd, DB_ERD / "database-erd.png")
        print("copied database-erd.png")
        # lightweight svg copy note
        src_svg = SVG / "erd_erd.svg"
        if src_svg.exists():
            shutil.copy(src_svg, DB_ERD / "database-erd.svg")


if __name__ == "__main__":
    main()
