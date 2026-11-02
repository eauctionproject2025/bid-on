# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

OUT = Path(__file__).resolve().parent
PNG = OUT.parent / "diagrams" / "exports" / "png"

MAPPING = [
    ("[Figure 3.1", "architecture.png"),
    ("[Figure 3.2", "deployment_deployment.png"),
    ("[Figure 3.3 — insert context", "dfd-context.png"),
    ("[Figure 3.3b", "dfd-level0.png"),
    ("[Figure 3.5", "activity_place-bid.png"),
    ("[Figure 3.6 — insert checkout", "sequence_checkout.png"),
    ("[Figure 3.6b", "sequence_login.png"),
    ("[Figure 3.7", "component_components.png"),
    ("[Figure 3.4", "erd_erd.png"),
    ("[Figure 3.8", "use-case.png"),
    ("[Figure 3.9", "class-domain.png"),
]


def main():
    doc = Document(OUT / "project-report.docx")
    replaced = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        for key, file in MAPPING:
            if t.startswith(key):
                path = PNG / file
                if path.exists():
                    p.text = ""
                    run = p.add_run()
                    run.add_picture(str(path), width=Inches(5.8))
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    replaced += 1
                break
    doc.save(OUT / "project-report.docx")
    print("embedded", replaced)


if __name__ == "__main__":
    main()
