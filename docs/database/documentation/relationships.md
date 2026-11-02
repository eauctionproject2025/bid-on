# Relationships — Bid On

| From | To | Cardinality | Notes |
|------|-----|-------------|-------|
| User | Auction (seller) | 1:N | `SellerAuctions` |
| User | Auction (winner) | 1:N | optional winner |
| User | Bid | 1:N | bidder |
| Category | Auction | 1:N | required category |
| Category | Category | 1:N | parent/children tree |
| Auction | Bid | 1:N | cascade delete |
| User | Watchlist | 1:N | cascade |
| Auction | Watchlist | 1:N | cascade; unique pair with user |
| User | Notification | 1:N | cascade |
| Auction | Transaction | 1:N | escrow rows |
| User | Transaction | 1:N | buyer and seller relations |
| Auction | Review | 1:N | |
| User | Review | 1:N | given and received |

## Business rules (enforced in app and/or schema)
- Only `pending` auctions may be approved or rejected by admin.
- Bids accepted only on `live` auctions meeting minimum next bid after row lock.
- Watchlist pair unique per user/auction.
- One review per (auction, fromUser).
- Stripe session id unique on Transaction when present.
- KYC/bank approval gates bidding/selling in application logic.
