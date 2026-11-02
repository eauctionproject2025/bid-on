# Test Cases Catalogue — Bid On

Legend: **V** = verified in this project cycle; **P** = partial / not formally executed at scale; **N** = not executed.

## Functional

| ID | Area | Steps (summary) | Expected | Status |
|----|------|-----------------|----------|--------|
| TC-AUTH-01 | Register | POST register with valid payload | 201 + user created unverified | V (API) |
| TC-AUTH-02 | Login | Login verified user | 200 + cookie/token | V |
| TC-AUC-01 | List live | GET /api/auctions | JSON auctions array | V (live Render) |
| TC-AUC-02 | Health | GET /api/health | ok true | V |
| TC-BID-01 | Min bid | Bid below minimum | 4xx error | P (unit/logic) |
| TC-PAY-01 | Checkout unpaid | session-status not paid | Frontend does not mark paid | V (code review + fix) |
| TC-ADM-01 | Reject live | Reject non-pending | 400 | V (code) |
| TC-UI-01 | Live site | Open bid-on.onrender.com/auctions | Shows catalogue UI | V |
| TC-NFR-01 | 5000 concurrent | Load test | — | N (not performed) |
| TC-NFR-02 | All pages &lt;3s cold start | Free Render wake | May exceed on cold start | P (observed wake delay) |

## Automated

Backend: `cd backend && npm test` (Vitest + Supertest; requires local Postgres + seed for full suite).  
Frontend: `cd frontend && npm test` (Vitest component/unit tests where present).

## Untested / future

- Full SMS notification delivery
- Stripe Connect seller payouts
- Formal penetration test
- Sustained load at 5000 concurrent users
