# API Documentation Summary (Bid On)

Base URL (production): `https://bid-on-api.onrender.com`  
Interactive OpenAPI UI: `/api/docs`  
Health: `GET /api/health` → `{ "ok": true, "service": "bid-on" }`

## Auth

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| POST | /api/auth/register | No | Returns verify guidance |
| POST | /api/auth/verify | No | Sets httpOnly cookie + token |
| POST | /api/auth/login | No | Cookie + JWT |
| POST | /api/auth/logout | No | Clears cookie |
| GET | /api/auth/me | Yes | Session hydrate |
| POST | /api/auth/forgot-password | No | OTP reset |
| POST | /api/auth/reset-password | No | |

## Core domain

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| GET | /api/auctions | Optional | Filters/search |
| GET | /api/auctions/:id | Optional | Detail + escrow snapshot |
| POST | /api/auctions | Seller | Create pending listing |
| PATCH | /api/auctions/:id | Seller/Admin | Edit rules by status |
| POST | /api/auctions/:id/approve | Admin | pending → live |
| POST | /api/auctions/:id/reject | Admin | pending only |
| POST | /api/auctions/:id/bids | Buyer | Row-locked bidding |
| GET | /api/categories | No | Tree + live counts |
| POST | /api/payments/create-checkout-session | Winner | Stripe or guarded dev mode |
| GET | /api/payments/session-status | Winner | Confirm paid → escrow |
| * | /api/admin/* | Admin | KPIs, users, CSV |

Authentication: `Authorization: Bearer <jwt>` and/or httpOnly `token` cookie with `credentials: include`.
