type Money = { toString(): string } | number | string | null | undefined;

function asNumber(value: Money, fallback = 0) {
  const n = Number(value ?? fallback);
  return Number.isFinite(n) ? n : fallback;
}

function roundMoney(n: number) {
  return Math.round(n * 100) / 100;
}

/** Lowest acceptable next bid. Opening bid may equal start price; later bids add the increment. */
export function minimumNextBid(auction: {
  currentBid: Money;
  startPrice: Money;
  minBidIncrement?: Money;
}) {
  const increment = Math.max(0.01, asNumber(auction.minBidIncrement, 1) || 1);
  const current = asNumber(auction.currentBid, 0);
  if (current <= 0) return roundMoney(asNumber(auction.startPrice, 0));
  return roundMoney(current + increment);
}
