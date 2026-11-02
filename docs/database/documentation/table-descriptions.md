# Table descriptions — Bid On logical schema

Runtime: PostgreSQL via Prisma. Academic exports: MySQL-compatible DDL + DBML under `docs/database/schema/`.

## User
Identity and compliance anchor. Unique email; bcrypt `passwordHash`; `Role` enum; email verification and password-reset OTP fields; optional phone/address; `suspended`; rating aggregates; parallel KYC and bank verification attribute groups with `VerificationStatus`.

## Category
Listing taxonomy. Unique `slug`; optional `parentId` for tree structure.

## Auction
Commercial listing. Seller and category FKs; title/description/images; Decimal pricing fields; `AuctionStatus`; schedule (`startsAt`, `endsAt`); optional `winnerId`; `rejectReason`; indexes on status, endsAt, categoryId.

## Bid
Immutable accepted bids. Auction and bidder FKs; Decimal `amount`; `createdAt`. Cascades on auction delete.

## Watchlist
Favourite junction. Unique (`userId`, `auctionId`).

## Notification
In-app alerts. `NotificationType`, message, read flag, optional JSON `meta`.

## Transaction
Escrow ledger. Auction/buyer/seller FKs; amount; Stripe identifiers; `TransactionStatus`; held/ship/release/dispute/resolve timestamps. Unique `stripeSessionId`.

## Review
Post-trade rating. Unique (`auctionId`, `fromUserId`); integer rating; optional comment.
