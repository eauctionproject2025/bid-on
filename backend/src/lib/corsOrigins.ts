/** Allowed browser origins for CORS / Socket.IO (comma-separated FRONTEND_URL). */
export function getCorsOrigins(): string[] {
  const raw = process.env.FRONTEND_URL || "http://localhost:3000";
  const fromEnv = raw
    .split(",")
    .map((s) => s.trim().replace(/\/$/, ""))
    .filter(Boolean);
  // Always allow local Next.js + the public Render frontend.
  const extras = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://bid-on.onrender.com",
  ];
  return [...new Set([...fromEnv, ...extras])];
}

/** Primary frontend origin (first FRONTEND_URL entry), no trailing slash. */
export function getFrontendOrigin(): string {
  return getCorsOrigins()[0] || "http://localhost:3000";
}
