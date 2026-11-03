/** Allowed browser origins for CORS / Socket.IO (comma-separated FRONTEND_URL). */
export function getCorsOrigins(): string[] {
  const raw = process.env.FRONTEND_URL || "http://localhost:3000";
  const fromEnv = raw
    .split(",")
    .map((s) => s.trim().replace(/\/$/, ""))
    .filter(Boolean);

  // Always allow the public Render site + local Next.js (local UI → live API is common).
  const always = [
    "https://bid-on.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
  ];

  return [...new Set([...fromEnv, ...always])];
}

/**
 * Primary frontend origin for verification / payment return links.
 * Prefer the live Render website over a stale Vercel URL in FRONTEND_URL.
 */
export function getFrontendOrigin(): string {
  const override = process.env.PUBLIC_APP_URL?.trim().replace(/\/$/, "");
  if (override) return override;

  const origins = getCorsOrigins();
  const renderSite = origins.find((o) => o === "https://bid-on.onrender.com");
  if (renderSite) return renderSite;

  const publicOrigin = origins.find(
    (o) => !o.includes("localhost") && !o.includes("127.0.0.1")
  );
  return publicOrigin || origins[0] || "http://localhost:3000";
}
