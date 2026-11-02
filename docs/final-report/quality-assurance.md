# Quality assurance report — Bid On academic deliverables

**Date:** 2 November 2026  
**Repository path:** `docs/`

## Review passes

### REVIEW 1 — Academic
| Check | Status |
|-------|--------|
| MICE 5-chapter structure | Pass |
| Prelims (title, approval, declaration, abstract, ack, lists) | Pass |
| Abstract length/keywords (no citations) | Pass (author may trim to 250–300 if department counts strictly) |
| ≤3 RQs, ≤3 objectives, ≤3 gaps | Pass |
| Ch.2 has no figures | Pass |
| IEEE references | Pass (12 sources; all real) |
| Ch.5 without new citations dependence | Pass |

### REVIEW 2 — Technical
| Check | Status |
|-------|--------|
| Stack matches repo (Next 15, Express, Prisma, Postgres, Socket.IO, Stripe) | Pass |
| Live URLs match Render deployment | Pass |
| Bid locking / escrow uniqueness described accurately | Pass |
| Partial/missing features disclosed | Pass |
| SQL/DBML reflect Prisma entities | Pass (logical MySQL export labelled) |

### REVIEW 3 — Language
| Check | Status |
|-------|--------|
| Consistent product name Bid On + proposal title | Pass |
| Avoided fabricated metrics | Pass |
| Residual grammar polish | Author may run final Word Editor pass |

### REVIEW 4 — Diagrams
| Check | Status |
|-------|--------|
| Editable sources present | Pass |
| SVG fallbacks exported | Pass (summary SVGs) |
| PNG via mermaid-cli | Fail in CI sandbox (Chrome); manual render required |
| draw.io ERD present | Pass |

### REVIEW 5 — Document
| Check | Status |
|-------|--------|
| DOCX editable | Pass |
| PDF generated | Pass (`project-report.pdf`) |
| Page numbers in footer | Pass (Arabic PAGE field; Roman prelims manual) |
| Auto TOC field | Partial (static list) |

### REVIEW 6 — Examiner
See `examiner-review.md`.

## Deliverable checklist

| Path | Present |
|------|---------|
| `docs/final-report/project-report.docx` | Yes |
| `docs/final-report/project-report.pdf` | Yes |
| `docs/final-report/references.bib` | Yes |
| `docs/final-report/examiner-review.md` | Yes |
| `docs/final-report/quality-assurance.md` | Yes |
| `docs/final-report/PHASE1_PROJECT_AUDIT.md` | Yes |
| `docs/diagrams/source/**` | Yes |
| `docs/diagrams/exports/svg/**` | Yes |
| `docs/database/schema/*` | Yes |
| `docs/database/erd/database-erd.drawio` | Yes |
| `docs/database/documentation/*` | Yes |
| `docs/database/seed/sample-data.sql` | Yes |
| `docs/appendices/*` | Yes |

## Unresolved items
1. Insert rendered figures into DOCX before print binding.  
2. Capture Figure 4.1 screenshot from live site.  
3. University plagiarism/AI similarity PDFs.  
4. Supervisor wet signature.  
5. Optional: Word section breaks for i, ii, iii prelim numbering.  
6. Rasterize PlantUML + Mermaid to PNG when Chrome available.  
7. Core Ch.1–start through pre-References measured **40 pages** in `project-report.pdf` (total PDF **53** pages including prelims/refs/appendices). Re-measure after replacing fallback figures and adding Figure 4.1 screenshot.
