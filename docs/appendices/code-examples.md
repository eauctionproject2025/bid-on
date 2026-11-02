# Selected Code Excerpts (Bid On)

These excerpts are taken from the repository and are illustrative, not complete files.

## Bid placement with row lock

File: `backend/src/routes/bids.ts`

```ts
await tx.$executeRaw`SELECT id FROM "Auction" WHERE id = ${auctionId} FOR UPDATE`;
const auction = await tx.auction.findUnique({ where: { id: auctionId } });
// validate live status, minimumNextBid, then create Bid and update currentBid
```

## Minimum next bid rule

File: `backend/src/lib/bidding.ts`

```ts
if (current <= 0) return roundMoney(asNumber(auction.startPrice, 0));
return roundMoney(current + increment);
```

## Frontend API base URL

File: `frontend/src/lib/api.ts`

```ts
export const API_URL = rawApiUrl || "http://localhost:4000";
```

Production builds should set `NEXT_PUBLIC_API_URL=https://bid-on-api.onrender.com`.
