# -*- coding: utf-8 -*-
"""Convert project-report.docx to PDF via Microsoft Word COM."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent
DOCX = OUT / "project-report.docx"
PDF = OUT / "project-report.pdf"


def main():
    import win32com.client  # type: ignore

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(DOCX))
        # 17 = wdFormatPDF
        doc.SaveAs(str(PDF), FileFormat=17)
        doc.Close(False)
        print("Wrote", PDF)
    finally:
        word.Quit()


if __name__ == "__main__":
    main()
