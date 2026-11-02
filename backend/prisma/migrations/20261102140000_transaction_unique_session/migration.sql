-- Prevent duplicate Stripe checkout sessions from creating multiple escrow rows.
CREATE UNIQUE INDEX IF NOT EXISTS "Transaction_stripeSessionId_key" ON "Transaction"("stripeSessionId");

-- Speed up escrow lookups by auction + lifecycle status.
CREATE INDEX IF NOT EXISTS "Transaction_auctionId_status_idx" ON "Transaction"("auctionId", "status");
