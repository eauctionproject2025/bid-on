# Database design documentation — Bid On

## Purpose
Independent academic deliverable describing the relational design implemented by `backend/prisma/schema.prisma` (PostgreSQL 16 on Render) and exported as MySQL-compatible DDL + DBML for examination portability.

## Design goals
1. Support the moderated auction lifecycle with clear status enumerations.
2. Preserve immutable bid history while maintaining `Auction.currentBid` for fast reads.
3. Encode escrow settlement as first-class `Transaction` rows.
4. Embed KYC/bank verification state on `User` for the current product scope.
5. Keep the schema examinable, normalizable, and extensible.

## Normalization notes
- 3NF-oriented entities for Auction, Bid, Transaction, Review, Watchlist, Notification, Category.
- Controlled redundancy: `currentBid` / `bidCount` on Auction updated inside the same DB transaction as Bid insert.
- KYC/bank fields on User avoid 1:1 tables while each user has at most one active dossier per type.

## Integrity
Foreign keys on all relations; unique constraints on email, category slug, watchlist pair, review pair, stripeSessionId; check-like behaviour via enums and application Zod validation.

## Performance
Indexes on Auction(status, endsAt, categoryId), Bid(auctionId, bidderId), Notification(userId, read), Transaction(auctionId+status, buyerId, sellerId). Bid path uses `SELECT … FOR UPDATE` on Auction.

## Scalability considerations
- Free-tier single Postgres instance; vertical scale first.
- Ephemeral local uploads are not a durable asset store — migrate KYC/images to object storage.
- Socket.IO on a single API instance; multi-instance would need a Redis adapter.
- Connect payouts would add Payout rows without replacing Transaction escrow history.

## Existing vs proposed improvements
| Area | Existing | Proposed (future) |
|------|----------|-------------------|
| KYC files | Path on disk / public uploads | Private object storage + DocumentAsset table |
| Seller payout | Ledger only | Stripe Connect + Payout table |
| Proxy bidding | Not present | Optional BidProxy settings |
| Analytics | Admin KPI/CSV | Optional event/warehouse feed |

Do not treat proposed tables as implemented.
