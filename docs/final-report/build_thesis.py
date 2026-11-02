# -*- coding: utf-8 -*-
"""Generate MICE/BICE-compliant Bid On thesis DOCX (Times New Roman, A4, IEEE cites)."""
from __future__ import annotations

from pathlib import Path

from chapters import ABSTRACT, CH1, CH2, CH3, CH4, CH5
from chapters_extra import (
    CH1_EXTRA,
    CH2_EXTRA,
    CH3_DB_EXTRA,
    CH3_EXTRA,
    CH4_EXTRA,
    CH5_EXTRA,
)
from chapters_long import IMPL_WALKTHROUGH, INTRO_CONTEXT, METHOD_QUALITY, RESULTS_NARRATIVE
from chapters_more import CH1_MORE, CH2_MORE, CH3_DIAGRAM_MORE, CH3_MORE, CH4_FINAL_MORE, CH4_MORE
from thesis_helpers import (
    add_caption,
    add_footer_page_numbers,
    add_heading_custom,
    add_page_break,
    add_para,
    add_table,
    paras,
    setup_doc,
)

OUT = Path(__file__).resolve().parent


def main():
    doc = setup_doc()

    # ---------- TITLE ----------
    for _ in range(2):
        add_para(doc, "", first_indent=False, space_after=0)
    add_para(
        doc,
        "The Next Generation e-Auction Management System: Enhancing Security, User Experience, and Data Analytics",
        size=16,
        bold=True,
        align="center",
        first_indent=False,
        space_after=18,
    )
    add_para(doc, "by", align="center", first_indent=False)
    add_para(doc, "Md Muktadir Rahman", align="center", bold=True, first_indent=False, space_after=0)
    add_para(doc, "Saima Shailin", align="center", bold=True, first_indent=False, space_after=0)
    add_para(doc, "Samir Asaf Smaran", align="center", bold=True, first_indent=False, space_after=18)
    add_para(
        doc,
        "MASTER OF SCIENCE IN INFORMATION AND COMMUNICATION TECHNOLOGY",
        align="center",
        bold=True,
        first_indent=False,
        space_after=6,
    )
    add_para(doc, "Department of Information and Communication Technology", align="center", first_indent=False, space_after=0)
    add_para(doc, "Faculty of Science and Technology", align="center", first_indent=False, space_after=0)
    add_para(doc, "BANGLADESH UNIVERSITY OF PROFESSIONALS", align="center", bold=True, first_indent=False, space_after=18)
    add_para(doc, "November 2026", align="center", first_indent=False)

    # ---------- APPROVAL ----------
    add_page_break(doc)
    add_heading_custom(doc, "APPROVAL", 0)
    add_para(
        doc,
        'The project titled “The Next Generation e-Auction Management System: Enhancing Security, User Experience, and Data Analytics” submitted by Md Muktadir Rahman (Roll No: 23549908004), Saima Shailin (Roll No: 23549908010), and Samir Asaf Smaran (Roll No: 23549908043), Session: 2022–2023, has been accepted as satisfactory for partial fulfillment of the requirement for the degree of Master of Science in Information and Communication Technology.',
        first_indent=False,
    )
    add_para(doc, "", first_indent=False)
    add_para(doc, "Lt Col Hussain Md Abu Nyeem, PhD, EME", bold=True, first_indent=False, space_after=0)
    add_para(doc, "Associate Professor", first_indent=False, space_after=0)
    add_para(doc, "Department of Electrical, Electronic and Communication Engineering", first_indent=False, space_after=0)
    add_para(doc, "Military Institute of Science and Technology (MIST)", first_indent=False, space_after=12)
    add_para(doc, "Supervisor", italic=True, first_indent=False)
    add_para(doc, "Date: ____________________", first_indent=False)

    # ---------- DECLARATION ----------
    add_page_break(doc)
    add_heading_custom(doc, "DECLARATION", 0)
    add_para(
        doc,
        "We hereby declare that this is our original work, and we have written it in its entirety. We have duly acknowledged all the sources of information that have been used in the thesis. This thesis (fully or partially) has not been submitted for any degree or diploma in any university or institute previously.",
        first_indent=False,
    )
    for name, rid in [
        ("Md Muktadir Rahman", "23549908004"),
        ("Saima Shailin", "23549908010"),
        ("Samir Asaf Smaran", "23549908043"),
    ]:
        add_para(doc, "", first_indent=False)
        add_para(doc, name, bold=True, first_indent=False, space_after=0)
        add_para(doc, f"ID: {rid}", first_indent=False, space_after=0)
        add_para(doc, "Department of Information and Communication Technology", first_indent=False, space_after=0)
        add_para(doc, "Faculty of Science and Technology", first_indent=False, space_after=0)
        add_para(doc, "Bangladesh University of Professionals", first_indent=False)

    # ---------- ACKNOWLEDGEMENT ----------
    add_page_break(doc)
    add_heading_custom(doc, "ACKNOWLEDGEMENTS", 0)
    add_para(
        doc,
        "First and foremost, we thank Almighty Allah for giving us the health and well-being needed to complete this project. We sincerely thank Lt Col Hussain Md Abu Nyeem, PhD, for his supervision, encouragement, patience, and guidance throughout the study and implementation of this work. We are grateful to the Department of Information and Communication Technology at Bangladesh University of Professionals for academic support. Finally, we thank our families and classmates for their continuous support and constructive feedback.",
        first_indent=False,
    )

    # ---------- ABSTRACT ----------
    add_page_break(doc)
    add_heading_custom(doc, "ABSTRACT", 0)
    add_para(doc, ABSTRACT, first_indent=False)
    add_para(
        doc,
        "Keywords: online auction, real-time bidding, escrow payment, PostgreSQL, Next.js, Express, Socket.IO, e-commerce security",
        italic=True,
        first_indent=False,
    )

    # ---------- TOC ----------
    add_page_break(doc)
    add_heading_custom(doc, "TABLE OF CONTENTS", 0)
    for t in [
        "APPROVAL",
        "DECLARATION",
        "ACKNOWLEDGEMENTS",
        "ABSTRACT",
        "LIST OF FIGURES",
        "LIST OF TABLES",
        "LIST OF ABBREVIATIONS",
        "CHAPTER 1. INTRODUCTION",
        "CHAPTER 2. LITERATURE REVIEW",
        "CHAPTER 3. METHODOLOGY",
        "CHAPTER 4. RESULTS ANALYSIS AND DISCUSSION",
        "CHAPTER 5. CONCLUSION AND FUTURE WORK",
        "REFERENCES",
        "APPENDICES",
    ]:
        add_para(doc, t, align="left", first_indent=False, space_after=2)

    add_page_break(doc)
    add_heading_custom(doc, "LIST OF FIGURES", 0)
    for fig in [
        "Figure 3.1  High-level system architecture of Bid On",
        "Figure 3.2  Deployment view on Render (Singapore)",
        "Figure 3.3  Context-level data flow diagram",
        "Figure 3.3b Level-0 data flow diagram",
        "Figure 3.4  Entity–relationship overview",
        "Figure 3.5  Activity flow for placing a bid",
        "Figure 3.6  Sequence diagram for winner checkout and escrow",
        "Figure 3.6b Sequence diagram for login and session issuance",
        "Figure 3.7  Component interactions between frontend and backend",
        "Figure 3.8  Use-case diagram (buyer, seller, admin)",
        "Figure 3.9  Domain class overview",
        "Figure 4.1  Live auctions catalogue on the deployed frontend",
    ]:
        add_para(doc, fig, align="left", first_indent=False, space_after=2)

    add_page_break(doc)
    add_heading_custom(doc, "LIST OF TABLES", 0)
    for tb in [
        "Table 2.1  Summary of related works on online auctions and e-commerce systems",
        "Table 3.1  Mapping of functional requirements to implemented modules",
        "Table 3.2  Core database entities and responsibilities",
        "Table 3.3  Technology stack used in Bid On",
        "Table 4.1  Experimental / deployment environment",
        "Table 4.2  Selected functional verification outcomes",
        "Table 4.3  Requirements coverage summary",
    ]:
        add_para(doc, tb, align="left", first_indent=False, space_after=2)

    add_page_break(doc)
    add_heading_custom(doc, "LIST OF ABBREVIATIONS", 0)
    for a, b in [
        ("API", "Application Programming Interface"),
        ("BDT", "Bangladeshi Taka"),
        ("BUP", "Bangladesh University of Professionals"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("DFD", "Data Flow Diagram"),
        ("ERD", "Entity–Relationship Diagram"),
        ("JWT", "JSON Web Token"),
        ("KYC", "Know Your Customer"),
        ("ORM", "Object–Relational Mapping"),
        ("REST", "Representational State Transfer"),
        ("RBAC", "Role-Based Access Control"),
        ("UI", "User Interface"),
    ]:
        add_para(doc, f"{a} — {b}", align="left", first_indent=False, space_after=2)

    # ===================== CHAPTER 1 =====================
    add_page_break(doc)
    add_heading_custom(doc, "CHAPTER 1", 0)
    add_heading_custom(doc, "INTRODUCTION", 0)
    add_heading_custom(doc, "1.1 Overview", 2)
    paras(doc, CH1["1.1"])
    add_heading_custom(doc, "1.2 Background/Motivation", 2)
    paras(doc, CH1["1.2"])
    add_heading_custom(doc, "1.3 Problem Statement", 2)
    paras(doc, CH1["1.3"])
    add_heading_custom(doc, "1.4 Research Questions", 2)
    for q in CH1["1.4"]:
        add_para(doc, q, first_indent=False)
    add_heading_custom(doc, "1.5 Research Objectives", 2)
    for o in CH1["1.5"]:
        add_para(doc, o, first_indent=False)
    add_heading_custom(doc, "1.6 Organization of the Thesis Paper", 2)
    paras(doc, CH1["1.6"])
    add_heading_custom(doc, "1.7 Scope and significance", 2)
    paras(doc, CH1_EXTRA)
    paras(doc, INTRO_CONTEXT)
    paras(doc, CH1_MORE)

    # ===================== CHAPTER 2 =====================
    add_page_break(doc)
    add_heading_custom(doc, "CHAPTER 2", 0)
    add_heading_custom(doc, "LITERATURE REVIEW", 0)
    add_heading_custom(doc, "2.1 Overview", 2)
    paras(doc, CH2["2.1"])
    add_heading_custom(doc, "2.2 Existing Works", 2)
    add_heading_custom(doc, "2.2.1 Electronic marketplaces and auction mechanisms", 2)
    paras(doc, CH2["2.2.1"])
    add_heading_custom(doc, "2.2.2 Web architectures for interactive applications", 2)
    paras(doc, CH2["2.2.2"])
    add_heading_custom(doc, "2.2.3 Security, identity, and payments", 2)
    paras(doc, CH2["2.2.3"])
    add_heading_custom(doc, "2.2.4 Summary table of related works", 2)
    paras(doc, CH2["2.2.4"])
    add_caption(doc, "Table 2.1: Summary of related works on online auctions and e-commerce systems")
    add_table(
        doc,
        ["Source", "Focus", "Method / type", "Limitation for this project"],
        [
            ["Sommerville [1]", "Software process & e-commerce context", "Textbook synthesis", "Broad guidance; not auction-specific"],
            ["Turban et al. [2]", "E-commerce mechanisms & UX", "Managerial/analytic", "Limited implementation blueprint"],
            ["IEEE Std 830 [7]", "Requirements specification", "Standard", "Not a system build"],
            ["Next.js / Express / Socket.IO / Prisma docs [4]–[6], [8]", "Implementation patterns", "Official documentation", "Vendor-specific"],
            ["Stripe Checkout [9]", "Payment delegation", "Official documentation", "Does not define full escrow domain model"],
            ["PostgreSQL / Render docs [11], [12]", "Data & hosting operations", "Official documentation", "Platform-specific"],
        ],
    )
    add_heading_custom(doc, "2.3 Research Gaps", 2)
    paras(doc, CH2["2.3"])
    add_heading_custom(doc, "2.4 Extended discussion of sources and baselines", 2)
    paras(doc, CH2_EXTRA)
    paras(doc, CH2_MORE)

    # ===================== CHAPTER 3 =====================
    add_page_break(doc)
    add_heading_custom(doc, "CHAPTER 3", 0)
    add_heading_custom(doc, "METHODOLOGY", 0)
    add_heading_custom(doc, "3.1 Overview", 2)
    paras(doc, CH3["3.1"])
    add_heading_custom(doc, "3.2 Requirements engineering and module mapping", 2)
    paras(doc, CH3["3.2"])
    add_caption(doc, "Table 3.1: Mapping of functional requirements to implemented modules")
    add_table(
        doc,
        ["ID", "Requirement", "Primary modules"],
        [
            ["FR1", "Registration / login", "auth routes; JWT/cookie session; OTP verify"],
            ["FR2", "Product listing + images", "auctions create/upload; Multer"],
            ["FR3", "Real-time bidding", "bids API; Socket.IO; bidding helper"],
            ["FR4", "Bid notifications", "Notification model; email verify; SMS not implemented"],
            ["FR5", "Payment gateway", "Stripe Checkout; Transaction escrow ledger"],
            ["FR6", "Search / filter", "GET /api/auctions query params"],
            ["FR7", "Feedback / rating", "Review model + APIs"],
            ["FR8", "Admin approval", "approve/reject auction endpoints"],
            ["FR9", "Countdown timer", "frontend Countdown component"],
            ["FR10", "Admin reports", "admin KPIs + CSV export"],
        ],
    )
    add_heading_custom(doc, "3.3 Proposed architecture", 2)
    paras(doc, CH3["3.3"])
    add_caption(doc, "Figure 3.1: High-level system architecture of Bid On (docs/diagrams/source/architecture.mmd).")
    add_para(doc, "[Figure 3.1 — insert rendered architecture diagram from docs/diagrams/exports here]", italic=True, align="center", first_indent=False)
    add_para(
        doc,
        "Figure 3.1 should be read left to right: the browser hosts the Next.js progressive interface; HTTPS REST calls and a Socket.IO channel reach the Express application tier; Prisma translates domain operations into PostgreSQL SQL; Stripe is contacted only for checkout session creation and payment-status confirmation. This separation keeps card data off the Bid On servers under ordinary Checkout usage.",
    )
    add_caption(doc, "Figure 3.2: Deployment view on Render (docs/diagrams/source/deployment/deployment.mmd).")
    add_para(doc, "[Figure 3.2 — insert rendered deployment diagram from docs/diagrams/exports here]", italic=True, align="center", first_indent=False)
    add_para(
        doc,
        "Figure 3.2 emphasizes regional co-location in Singapore and the GitHub-to-Render deployment path. Examiners verifying the live system should expect free-tier cold starts on the web and API services after idle periods; the database service remains the durable store for auctions and bids across process sleeps.",
    )
    add_caption(doc, "Table 3.3: Technology stack used in Bid On")
    add_table(
        doc,
        ["Layer", "Technologies"],
        [
            ["Frontend", "Next.js 15, React 19, TypeScript, Tailwind, TanStack Query, Zustand, Socket.IO client, Axios"],
            ["Backend", "Express 5, Prisma 5, Zod, JWT + httpOnly cookies, Multer, Socket.IO, Stripe SDK"],
            ["Database", "PostgreSQL 16 (Render bid-on-db, Singapore)"],
            ["Hosting", "Render services bid-on (web) and bid-on-api (API)"],
            ["Tooling", "GitHub, Vitest, OpenAPI/Swagger UI at /api/docs"],
        ],
    )
    add_heading_custom(doc, "3.4 Process and interaction models", 2)
    paras(doc, CH3["3.4"])
    add_caption(doc, "Figure 3.3: Context-level DFD (docs/diagrams/source/dfd-context.mmd).")
    add_para(doc, "[Figure 3.3 — insert context DFD]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.3b: Level-0 DFD (docs/diagrams/source/dfd-level0.mmd).")
    add_para(doc, "[Figure 3.3b — insert Level-0 DFD]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.5: Activity — place bid (docs/diagrams/source/activity/place-bid.mmd).")
    add_para(doc, "[Figure 3.5 — insert place-bid activity diagram]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.6: Sequence — checkout/escrow (docs/diagrams/source/sequence/checkout.mmd).")
    add_para(doc, "[Figure 3.6 — insert checkout sequence diagram]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.6b: Sequence — login (docs/diagrams/source/sequence/login.mmd).")
    add_para(doc, "[Figure 3.6b — insert login sequence diagram]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.7: Components (docs/diagrams/source/component/components.mmd).")
    add_para(doc, "[Figure 3.7 — insert component diagram]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.8: Use cases (docs/diagrams/source/use-case.puml).")
    add_para(doc, "[Figure 3.8 — insert use-case diagram]", italic=True, align="center", first_indent=False)
    add_caption(doc, "Figure 3.9: Domain classes (docs/diagrams/source/class-domain.mmd).")
    add_para(doc, "[Figure 3.9 — insert domain class diagram]", italic=True, align="center", first_indent=False)
    paras(doc, CH3_DIAGRAM_MORE)

    add_heading_custom(doc, "3.5 Database design and implementation", 2)
    paras(doc, CH3["3.5"])
    add_caption(doc, "Table 3.2: Core database entities and responsibilities")
    add_table(
        doc,
        ["Entity", "Responsibility"],
        [
            ["User", "Identity, RBAC, KYC/bank verification dossier, rating aggregates"],
            ["Category", "Taxonomy tree for listings"],
            ["Auction", "Listing content, pricing rules, clock, status, winner"],
            ["Bid", "Immutable accepted bid history"],
            ["Watchlist", "User–auction favourites (unique pair)"],
            ["Notification", "Typed in-app alerts"],
            ["Transaction", "Escrow ledger with Stripe identifiers and lifecycle timestamps"],
            ["Review", "Post-trade ratings unique per auction and reviewer"],
        ],
    )
    add_caption(doc, "Figure 3.4: Entity–relationship overview (docs/diagrams/source/erd/erd.mmd; draw.io under docs/database/erd/).")
    add_para(doc, "[Figure 3.4 — insert ERD from docs/database/erd or docs/diagrams/exports/svg/erd_erd.svg]", italic=True, align="center", first_indent=False)

    add_heading_custom(doc, "3.5.1 Bidding algorithm (implementation method)", 2)
    add_para(
        doc,
        "Minimum next bid is computed from the auction’s currentBid and minBidIncrement. If currentBid is zero, the next acceptable amount equals startPrice; otherwise it equals currentBid plus increment, with monetary rounding applied in the bidding helper module. On POST /api/auctions/:id/bids, the API authenticates the buyer, enforces compliance gates, begins a database transaction, locks the auction row, re-reads auction state, validates live status and amount, inserts a Bid, updates currentBid and bidCount, commits, then emits Socket.IO events so connected clients observe a single consistent order of acceptance.",
    )
    add_para(
        doc,
        "This algorithm is intentionally simple and auditable. It does not implement proxy bidding or second-price sealed mechanisms. Those alternatives remain outside the requirements chart and are noted only to clarify scope.",
    )

    add_heading_custom(doc, "3.5.2 Escrow state method", 2)
    add_para(
        doc,
        "When a winner initiates checkout, the API creates a Stripe Checkout session (or a guarded development substitute when explicitly enabled). On session-status confirmation, the API verifies that the processor reports a completed and paid session before creating or updating a Transaction in held state and associating stripeSessionId uniquely. Subsequent dispute, release, and completion transitions update timestamps and status enumerations so that administrators can inspect settlement progress without reconstructing browser history.",
    )

    add_heading_custom(doc, "3.6 Security and compliance method", 2)
    paras(doc, CH3["3.6"])
    add_heading_custom(doc, "3.7 Implementation method", 2)
    paras(doc, CH3["3.7"])
    paras(doc, CH3_EXTRA)
    add_heading_custom(doc, "3.7.1 Extended entity notes", 2)
    paras(doc, CH3_DB_EXTRA)
    add_heading_custom(doc, "3.7.2 Functional requirement implementation walkthrough", 2)
    paras(doc, IMPL_WALKTHROUGH)
    add_heading_custom(doc, "3.7.3 Quality assurance method during construction", 2)
    paras(doc, METHOD_QUALITY)
    add_heading_custom(doc, "3.7.4 Additional methodological notes", 2)
    paras(doc, CH3_MORE)
    add_heading_custom(doc, "3.8 Summary of the Chapter", 2)
    paras(doc, CH3["3.8"])

    # ===================== CHAPTER 4 =====================
    add_page_break(doc)
    add_heading_custom(doc, "CHAPTER 4", 0)
    add_heading_custom(doc, "RESULTS ANALYSIS AND DISCUSSION", 0)
    add_heading_custom(doc, "4.1 Overview", 2)
    paras(doc, CH4["4.1"])
    add_heading_custom(doc, "4.2 Experimental setup", 2)
    paras(doc, CH4["4.2"])
    add_caption(doc, "Table 4.1: Experimental / deployment environment")
    add_table(
        doc,
        ["Component", "Configuration"],
        [
            ["Frontend", "Next.js 15 on Render service bid-on — https://bid-on.onrender.com"],
            ["API", "Express/Prisma on bid-on-api — https://bid-on-api.onrender.com"],
            ["Database", "PostgreSQL 16 bid-on-db (Singapore)"],
            ["Repository", "https://github.com/eauctionproject2025/bid-on"],
            ["Local tooling", "Node.js 22+, Git, Render CLI, Vitest"],
        ],
    )
    add_heading_custom(doc, "4.3 Functional verification results", 2)
    paras(doc, CH4["4.3"])
    add_caption(doc, "Table 4.2: Selected functional verification outcomes")
    add_table(
        doc,
        ["Check", "Expected", "Result"],
        [
            ["GET /api/health", "{ok:true}", "Pass (live)"],
            ["GET /api/auctions", "Live lots JSON", "Pass (live)"],
            ["Website /auctions", "Catalogue UI renders", "Pass (live)"],
            ["Checkout confirm", "Paid only if Stripe session complete+paid", "Pass (logic verified)"],
            ["Reject non-pending", "HTTP 400", "Pass (logic verified)"],
            ["Bid row lock path", "Serialized accept under concurrency", "Pass (code/path present)"],
            ["Cold start < 3s", "All pages after idle", "Partial / Fail vs NFR4"],
            ["5000 concurrent users", "Sustained load", "Not tested"],
        ],
    )
    add_caption(doc, "Figure 4.1: Live auctions catalogue on the deployed frontend (https://bid-on.onrender.com/auctions).")
    add_para(doc, "[Figure 4.1 — insert screenshot of https://bid-on.onrender.com/auctions captured at submission time]", italic=True, align="center", first_indent=False)
    add_heading_custom(doc, "4.3.1 Expanded verification narrative", 2)
    paras(doc, RESULTS_NARRATIVE)
    add_heading_custom(doc, "4.4 Comparative discussion against requirements", 2)
    paras(doc, CH4["4.4"])
    add_caption(doc, "Table 4.3: Requirements coverage summary")
    add_table(
        doc,
        ["Status", "Items"],
        [
            ["Implemented", "Auth, listings, live bidding, Stripe/escrow path, search/filter, ratings, admin approval, countdown, admin CSV/KPIs"],
            ["Partial", "Notifications without SMS; performance under sleep/wake"],
            ["Not implemented / not tested", "AI fraud detection; Connect payouts; formal 5000-user load test"],
        ],
    )
    add_heading_custom(doc, "4.5 Security and payment discussion", 2)
    paras(doc, CH4["4.5"])
    add_heading_custom(doc, "4.5.1 Multi-lens discussion and threats to validity", 2)
    paras(doc, CH4_EXTRA)
    paras(doc, CH4_MORE)
    add_heading_custom(doc, "4.5.2 Research questions revisited", 2)
    paras(doc, CH4_FINAL_MORE)
    add_heading_custom(doc, "4.6 Summary of the Chapter", 2)
    paras(doc, CH4["4.6"])

    # ===================== CHAPTER 5 =====================
    add_page_break(doc)
    add_heading_custom(doc, "CHAPTER 5", 0)
    add_heading_custom(doc, "CONCLUSION AND FUTURE WORK", 0)
    add_heading_custom(doc, "5.1 Research summary", 2)
    paras(doc, CH5["5.1"])
    add_heading_custom(doc, "5.2 Major findings", 2)
    paras(doc, CH5["5.2"])
    add_heading_custom(doc, "5.3 Achievement of research objectives", 2)
    for o in CH5["5.3"]:
        add_para(doc, o, first_indent=False)
    add_heading_custom(doc, "5.4 Contributions of the study", 2)
    paras(doc, CH5["5.4"])
    add_heading_custom(doc, "5.5 Limitations", 2)
    paras(doc, CH5["5.5"])
    add_heading_custom(doc, "5.6 Future recommendations", 2)
    paras(doc, CH5["5.6"])
    paras(doc, CH5_EXTRA)

    # ===================== REFERENCES =====================
    add_page_break(doc)
    add_heading_custom(doc, "REFERENCES", 0)
    for r in [
        "[1] I. Sommerville, Software Engineering, 10th ed. Boston, MA, USA: Pearson, 2016.",
        "[2] E. Turban, J. Outland, D. King, J. K. Lee, T.-P. Liang, and D. C. Turban, Electronic Commerce 2018: A Managerial and Social Networks Perspective, 9th ed. Cham, Switzerland: Springer, 2018.",
        "[3] Project team, “Online Auction System Requirement Chart,” internal requirements artefact, Bangladesh University of Professionals, Dhaka, Bangladesh, 2024.",
        "[4] Vercel Inc., “Next.js Documentation.” [Online]. Available: https://nextjs.org/docs. [Accessed: 02-Nov-2026].",
        "[5] OpenJS Foundation, “Express — Node.js web application framework.” [Online]. Available: https://expressjs.com. [Accessed: 02-Nov-2026].",
        "[6] Socket.IO, “Socket.IO Documentation.” [Online]. Available: https://socket.io/docs. [Accessed: 02-Nov-2026].",
        "[7] IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications. New York, NY, USA: IEEE, 1998.",
        "[8] Prisma Data Inc., “Prisma Documentation.” [Online]. Available: https://www.prisma.io/docs. [Accessed: 02-Nov-2026].",
        "[9] Stripe Inc., “Checkout.” [Online]. Available: https://stripe.com/docs/payments/checkout. [Accessed: 02-Nov-2026].",
        "[10] eauctionproject2025, bid-on. GitHub. [Online]. Available: https://github.com/eauctionproject2025/bid-on. [Accessed: 02-Nov-2026].",
        "[11] Render, “Render Documentation.” [Online]. Available: https://render.com/docs. [Accessed: 02-Nov-2026].",
        "[12] PostgreSQL Global Development Group, “PostgreSQL 16 Documentation.” [Online]. Available: https://www.postgresql.org/docs/16/. [Accessed: 02-Nov-2026].",
    ]:
        add_para(doc, r, align="left", first_indent=False, space_after=6)

    # ===================== APPENDICES =====================
    add_page_break(doc)
    add_heading_custom(doc, "APPENDICES", 0)
    add_heading_custom(doc, "Appendix A — Repository documentation map", 2)
    add_para(
        doc,
        "docs/final-report (this thesis DOCX/PDF and audit notes), docs/database (SQL/DBML/ERD/docs/seed), docs/diagrams (editable Mermaid/PlantUML sources and exports), docs/appendices (API and test catalogues), docs/DEPLOY.md (hosting runbook), backend/prisma/schema.prisma (runtime schema).",
        first_indent=False,
    )
    add_heading_custom(doc, "Appendix B — Representative API surface", 2)
    add_para(
        doc,
        "Production API base: https://bid-on-api.onrender.com. Interactive OpenAPI UI: /api/docs. Authentication uses Authorization Bearer and/or httpOnly cookie with credentials included.",
        first_indent=False,
    )
    add_table(
        doc,
        ["Method", "Path", "Auth", "Notes"],
        [
            ["GET", "/api/health", "No", "Service liveness"],
            ["POST", "/api/auth/register", "No", "Create unverified user"],
            ["POST", "/api/auth/verify", "No", "OTP verify; cookie + token"],
            ["POST", "/api/auth/login", "No", "Cookie + JWT"],
            ["POST", "/api/auth/logout", "No", "Clear cookie"],
            ["GET", "/api/auth/me", "Yes", "Session hydrate"],
            ["POST", "/api/auth/forgot-password", "No", "OTP reset start"],
            ["POST", "/api/auth/reset-password", "No", "OTP reset complete"],
            ["GET", "/api/auctions", "Optional", "Search/filter catalogue"],
            ["GET", "/api/auctions/:id", "Optional", "Detail + escrow snapshot"],
            ["POST", "/api/auctions", "Seller", "Create pending listing"],
            ["PATCH", "/api/auctions/:id", "Seller/Admin", "Edit by status rules"],
            ["POST", "/api/auctions/:id/approve", "Admin", "pending → live"],
            ["POST", "/api/auctions/:id/reject", "Admin", "pending only"],
            ["POST", "/api/auctions/:id/bids", "Buyer", "Row-locked bidding"],
            ["GET", "/api/categories", "No", "Tree + live counts"],
            ["POST", "/api/payments/create-checkout-session", "Winner", "Stripe or guarded dev"],
            ["GET", "/api/payments/session-status", "Winner", "Confirm paid → escrow"],
            ["*", "/api/admin/*", "Admin", "KPIs, users, CSV"],
        ],
    )
    add_heading_custom(doc, "Appendix C — Test case catalogue", 2)
    add_para(
        doc,
        "Legend: V = verified in this project cycle; P = partial; N = not executed. Automated suites: backend Vitest/Supertest; frontend Vitest where present.",
        first_indent=False,
    )
    add_table(
        doc,
        ["ID", "Area", "Expected", "Status"],
        [
            ["TC-AUTH-01", "Register", "201 + unverified user", "V"],
            ["TC-AUTH-02", "Login", "200 + cookie/token", "V"],
            ["TC-AUC-01", "List live", "JSON auctions array", "V (live)"],
            ["TC-AUC-02", "Health", "ok true", "V (live)"],
            ["TC-BID-01", "Min bid", "4xx below minimum", "P"],
            ["TC-PAY-01", "Unpaid session", "UI does not mark paid", "V"],
            ["TC-ADM-01", "Reject live", "400", "V"],
            ["TC-UI-01", "Live site", "Catalogue UI", "V"],
            ["TC-NFR-01", "5000 users", "Sustained load", "N"],
            ["TC-NFR-02", "Cold start <3s", "All pages", "P"],
        ],
    )
    add_heading_custom(doc, "Appendix D — Selected implementation excerpts", 2)
    add_para(
        doc,
        "Bid placement locks the auction row before validation (backend/src/routes/bids.ts). Minimum next bid is computed in backend/src/lib/bidding.ts. Frontend API base URL is resolved from NEXT_PUBLIC_API_URL in frontend/src/lib/api.ts. Excerpts and commentary: docs/appendices/code-examples.md.",
        first_indent=False,
    )
    add_heading_custom(doc, "Appendix E — Independent database pack", 2)
    add_para(
        doc,
        "MySQL-compatible DDL: docs/database/schema/database-schema.sql. DBML: docs/database/schema/database-schema.dbml. Editable ERD: docs/database/erd/database-erd.drawio. Narrative: docs/database/documentation/*.md. Seed: docs/database/seed/sample-data.sql. These artefacts describe the logical schema corresponding to the Prisma/PostgreSQL implementation; runtime production remains PostgreSQL.",
        first_indent=False,
    )
    add_heading_custom(doc, "Appendix F — Column summary for core tables", 2)
    add_para(doc, "The following summary supports examiners who read the thesis without opening Prisma. It is not a substitute for the SQL/DBML pack.", first_indent=False)
    add_table(
        doc,
        ["Table", "Key columns (selected)"],
        [
            ["User", "id, name, email, passwordHash, role, verified, otp*, suspended, ratingAvg/Count, kyc*, bank*, timestamps"],
            ["Category", "id, name, slug, parentId"],
            ["Auction", "id, sellerId, categoryId, title, description, images[], prices, currentBid, minBidIncrement, bidCount, status, startsAt, endsAt, winnerId, rejectReason"],
            ["Bid", "id, auctionId, bidderId, amount, createdAt"],
            ["Watchlist", "id, userId, auctionId, createdAt (unique user+auction)"],
            ["Notification", "id, userId, type, message, read, meta, createdAt"],
            ["Transaction", "id, auctionId, buyerId, sellerId, amount, stripe*, status, held/ship/release/dispute timestamps"],
            ["Review", "id, auctionId, fromUserId, toUserId, rating, comment, createdAt"],
        ],
    )

    add_footer_page_numbers(doc)
    out_docx = OUT / "project-report.docx"
    doc.save(out_docx)
    print("Wrote", out_docx)


if __name__ == "__main__":
    main()
