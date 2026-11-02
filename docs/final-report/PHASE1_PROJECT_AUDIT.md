# Phase 1 — Project Audit (Bid On / e-Auction)

**Programme:** MICT — Bangladesh University of Professionals (BUP), Department of ICT  
**Working title (from proposal):** *The Next Generation e-Auction Management System: Enhancing Security, User Experience, and Data Analytics*  
**Implementation repo:** https://github.com/eauctionproject2025/bid-on  
**Live system:** https://bid-on.onrender.com (UI), https://bid-on-api.onrender.com (API)  
**Audit date:** 2 November 2026  

---

## 1. University formatting authority (MICE/BICE Thesis Guidelines)

The university module is **primary**. It **overrides** the longer 9-chapter / ~80-page outline in the prompt.

| Requirement | University rule |
|-------------|-----------------|
| Chapter sequence | Title → Approval → Declaration → Abstract → Acknowledgement → ToC → List of Tables → List of Figures → **Ch.1 Introduction → Ch.2 Literature Review → Ch.3 Methodology → Ch.4 Results and Discussion → Ch.5 Conclusion and Future Work** → References → Appendices |
| Length | **40–60 pages** from Introduction through Conclusion (prelims/refs excluded) |
| Paper | A4; margins L 1.5″ / R·T·B 1.0″; 1.5 line spacing; justified; Times New Roman 12 pt body / 14 pt bold headings |
| Page numbers | Bottom centre; Roman for prelims; Arabic from Ch.1 |
| Abstract | 250–300 words, one paragraph, 5–7 keywords; no citations/figures |
| Citations | **IEEE** sequential `[1]`, `[2]` |
| Similarity / AI | Each **&lt; 25%** (Abstract + Ch.1–5); report must be submitted |
| Supervisor | Signature required (proposal names Lt Col Hussain Md Abu Nyeem, PhD) |
| Ch.2 | **No figures**; literature summary **table** required; ≤3 research gaps |
| Ch.3 | Architecture + flowchart/block diagrams; high-quality labelled figures |
| Ch.4 | Experimental setup, results, discussion (software project: functional evaluation, not ML metrics) |
| Ch.5 | Map findings to objectives; limitations; future work; **no references** |

**Decision:** Produce a **MICE-compliant 5-chapter thesis book (~45–55 core pages)** plus separate technical packs (diagrams, SQL/DBML, API, tests) so examiners still receive the independent database/architecture deliverables requested.

---

## 2. Stakeholder / identity facts (from proposal PDF)

| Role | Details |
|------|---------|
| Members | Md Muktadir Rahman (23549908004), Saima Shailin (23549908010), Samir Asaf Smaran (23549908043) |
| Session | 2022–2023 |
| Supervisor (proposal) | Lt Col Hussain Md Abu Nyeem, PhD, Associate Professor, EECE, MIST |
| Product name in code | **Bid On** |

*Placeholders remain for signature dates if the department requires a specific submission date.*

---

## 3. Implemented technology stack (verified in repo)

| Layer | Actual stack |
|-------|----------------|
| Frontend | Next.js 15 (App Router), React 19, TypeScript, Tailwind, TanStack Query, Zustand, Socket.IO client, Axios |
| Backend | Express 5, Prisma 5, PostgreSQL 16, Socket.IO, Zod, JWT + httpOnly cookies, Multer, Stripe |
| Hosting | Render: `bid-on` (web), `bid-on-api` (API), `bid-on-db` (Postgres, Singapore) |
| Docs in repo | `DEPLOY.md`, `DATABASE_ARCHITECTURE.md/.html`, OpenAPI/Swagger at `/api/docs` |

---

## 4. Requirements coverage (Requirement Chart vs implementation)

| ID | Requirement | Priority | Status in Bid On |
|----|-------------|----------|------------------|
| FR1 | Registration / login | High | Implemented (email verify OTP) |
| FR2 | Product listing + images | High | Implemented (seller create + images) |
| FR3 | Real-time bidding | High | Implemented (HTTP + Socket.IO) |
| FR4 | Bid notifications email/SMS | Medium | **Partial** — in-app + email verify; SMS **not** implemented |
| FR5 | Payment gateway | High | Stripe Checkout + escrow ledger; Connect payout **Phase-2** |
| FR6 | Search / filter | High | Implemented on auctions |
| FR7 | Feedback / rating | Medium | Implemented (Review model) |
| FR8 | Admin approval of listings | High | Implemented |
| FR9 | Countdown timer | High | Implemented |
| FR10 | Admin reports/analytics | Medium | KPI/admin + CSV export |
| NFR1 | Mobile responsive | High | Responsive UI (qualitative) |
| NFR2 | 5000 concurrent users | High | **Not load-tested** at that scale (must state honestly) |
| NFR3 | Encryption for transactions | High | HTTPS + hashed passwords + JWT; Stripe PCI offload |
| NFR4 | Page load &lt; 3s | High | **Not formally benchmarked** across all pages |
| Dep. | AI fraud detection | — | **Not implemented** (future work) |

**Geographic scope (requirements):** Bangladesh / Asia; currency handling primarily BDT in UI with Stripe currency config.

---

## 5. Existing documentation gaps

| Area | Gap |
|------|-----|
| Formal thesis book | Missing DOCX/PDF aligned to MICE 5-chapter structure |
| Literature review | No academic LR table / IEEE refs in repo |
| Use-case / sequence / DFD sources | Not present as editable diagram pack |
| Independent MySQL DDL / DBML / draw.io ERD | Only Prisma schema + earlier architecture MD |
| Formal test-case catalogue | Backend Vitest exists; no examiner-style UAT matrix |
| Screenshots/results chapter | Live system exists but not yet packaged as evaluation evidence |
| Proposal vs code naming | Proposal “e-AMS” vs product “Bid On” — report will map both |

---

## 6. Technical inconsistencies / honesty constraints

1. Free Render web services **sleep** after idle; first request latency can exceed NFR “&lt;3s”.  
2. Uploaded images on free instance are **ephemeral**; KYC files under public `/uploads` (privacy limitation).  
3. Escrow **ledger** is implemented; automated **Stripe Connect seller payout** is not.  
4. SMS notifications and AI fraud detection appear in early requirements/dependencies but are **out of scope** of the current build.  
5. Do **not** claim 5000-user load tests or fabricated experimental results.

---

## 7. Proposed thesis outline (MICE-compliant)

1. Prelims (Title, Approval, Declaration, Abstract, Acknowledgement, ToC, Lists, Abbreviations)  
2. **Chapter 1 — Introduction** (overview, background, problem, ≤3 RQs, ≤3 objectives, organisation)  
3. **Chapter 2 — Literature Review** (grouped works + summary table + ≤3 gaps; **no figures**)  
4. **Chapter 3 — Methodology** (requirements mapping, architecture, DB design, security, implementation method, diagrams)  
5. **Chapter 4 — Results Analysis and Discussion** (setup, functional/test evidence, comparison to requirements, limitations)  
6. **Chapter 5 — Conclusion** (objectives achieved, contributions, limitations, future work)  
7. References (IEEE) + Appendices (API, extended schema notes, selected code)  

**Separate packs (not stuffed only as screenshots):** `docs/diagrams/`, `docs/database/`, `docs/appendices/`, `docs/final-report/`.

---

## 8. Proposed diagram list (editable sources)

| ID | Diagram | Format |
|----|---------|--------|
| Fig 3.x | System / deployment architecture | `.mmd` + SVG |
| Fig 3.x | Use-case (buyer/seller/admin) | `.puml` + SVG |
| Fig 3.x | Activity — place bid / checkout escrow | `.mmd` |
| Fig 3.x | Sequence — login, bid, payment | `.mmd` |
| Fig 3.x | DFD context + Level-0 | `.mmd` |
| Fig 3.x | Component diagram | `.mmd` |
| Fig 3.x / DB pack | ERD | `.dbml` + `.drawio` + SVG/PNG |
| Fig 3.x | Class (domain) | `.puml` |

Ch.2 remains figure-free per guidelines.

---

## 9. Database assessment (high level)

**Existing (Prisma/PostgreSQL):** User, Category, Auction, Bid, Watchlist, Notification, Transaction (escrow), Review — with enums for role, auction status, verification, notification, transaction status. Money as `Decimal(12,2)`. Bid path uses row locking; `Transaction.stripeSessionId` unique.

**Independent deliverables planned:** MySQL-compatible DDL (logical equivalent), DBML, draw.io ERD, table/relationship docs, optional seed SQL — clearly labelled as **logical export of the implemented Prisma/Postgres design** (runtime DB is PostgreSQL on Render).

---

## 10. Proceed / questions

**Proceeding to Phases 2–6** with MICE 5-chapter structure and separate technical packs.

**Optional confirmations (will use proposal data unless corrected):**
1. Final title string for the title page (keep proposal title or shorten to “Bid On: A Secure Real-Time e-Auction Management System”)?  
2. Exact submission date for signature blocks?  
3. Co-supervisor remains N/A?

---

*End of Phase 1 audit*
