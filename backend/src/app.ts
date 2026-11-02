import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import path from "path";
import authRoutes from "./routes/auth";
import userRoutes from "./routes/users";
import categoryRoutes from "./routes/categories";
import auctionRoutes from "./routes/auctions";
import bidRoutes from "./routes/bids";
import watchlistRoutes from "./routes/watchlist";
import notificationRoutes from "./routes/notifications";
import reviewRoutes from "./routes/reviews";
import paymentRoutes, { handleStripeWebhook } from "./routes/payments";
import adminRoutes from "./routes/admin";
import { errorHandler } from "./lib/asyncHandler";
import { mountSwagger } from "./docs/swagger";
import { getCorsOrigins } from "./lib/corsOrigins";

export function createApp() {
  const app = express();
  const corsOrigins = getCorsOrigins();

  app.post(
    "/api/payments/webhook",
    express.raw({ type: "application/json" }),
    async (req, res) => {
      try {
        const sig = req.headers["stripe-signature"] as string;
        await handleStripeWebhook(req.body as Buffer, sig);
        res.json({ received: true });
      } catch (err) {
        console.error(err);
        res.status(400).send(`Webhook Error`);
      }
    }
  );

  app.use(
    cors({
      origin: corsOrigins.length === 1 ? corsOrigins[0] : corsOrigins,
      credentials: true,
    })
  );
  app.use(express.json());
  app.use(cookieParser());
  app.use("/uploads", express.static(path.resolve(process.env.UPLOAD_DIR || "uploads")));

  mountSwagger(app);

  app.get("/", (_req, res) => {
    res.type("html").send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bid On API</title>
  <style>
    :root { color-scheme: dark; }
    body { margin:0; font-family: ui-sans-serif, system-ui, sans-serif; background:#0b1220; color:#e8eefc; }
    main { max-width: 720px; margin: 0 auto; padding: 48px 20px; }
    h1 { font-size: 2rem; margin: 0 0 8px; }
    .muted { color:#9db0d0; }
    .ok { display:inline-block; background:#12351f; color:#6dffb0; padding:4px 10px; border-radius:999px; font-size:12px; margin-bottom:16px; }
    a { color:#7eb6ff; }
    .card { background:#121a2b; border:1px solid #243147; border-radius:12px; padding:16px; margin-top:16px; }
    .lot { display:flex; gap:12px; align-items:flex-start; }
    .lot img { width:88px; height:88px; object-fit:cover; border-radius:8px; background:#1a2438; }
    .price { font-weight:700; color:#ffd27a; }
    ul { padding-left: 18px; }
    code { background:#1a2438; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <main>
    <div class="ok" id="status">Checking…</div>
    <h1>Bid On API</h1>
    <p class="muted">Live Express + Prisma backend on Render.</p>
    <ul>
      <li><a href="/api/health">/api/health</a></li>
      <li><a href="/api/docs">/api/docs</a> (Swagger)</li>
      <li><a href="/api/auctions">/api/auctions</a></li>
      <li><a href="/api/categories">/api/categories</a></li>
    </ul>
    <div class="card">
      <h2 style="margin:0 0 12px; font-size:1.1rem;">Live auctions</h2>
      <div id="auctions" class="muted">Loading…</div>
    </div>
  </main>
  <script>
    async function load() {
      const status = document.getElementById('status');
      const box = document.getElementById('auctions');
      try {
        const h = await fetch('/api/health').then(r => r.json());
        status.textContent = h.ok ? 'LIVE' : 'DOWN';
        const data = await fetch('/api/auctions').then(r => r.json());
        const list = data.auctions || [];
        if (!list.length) { box.textContent = 'No live auctions yet.'; return; }
        box.innerHTML = list.map(a => {
          const img = (a.images && a.images[0]) || '';
          const bid = Number(a.currentBid || a.startPrice || 0).toLocaleString();
          return '<div class="lot">' +
            (img ? '<img src="'+img+'" alt="" />' : '') +
            '<div><strong>'+a.title+'</strong><div class="muted">'+(a.category?.name||'')+' · '+(a.seller?.name||'')+'</div>' +
            '<div class="price">BDT '+bid+'</div></div></div>';
        }).join('<hr style="border:0;border-top:1px solid #243147;margin:12px 0" />');
      } catch (e) {
        status.textContent = 'ERROR';
        box.textContent = String(e);
      }
    }
    load();
  </script>
</body>
</html>`);
  });

  app.get("/api/health", (_req, res) => res.json({ ok: true, service: "bid-on" }));

  app.use("/api/auth", authRoutes);
  app.use("/api/users", userRoutes);
  app.use("/api/categories", categoryRoutes);
  app.use("/api/auctions", auctionRoutes);
  app.use("/api/auctions/:id/bids", bidRoutes);
  app.use("/api/watchlist", watchlistRoutes);
  app.use("/api/notifications", notificationRoutes);
  app.use("/api/reviews", reviewRoutes);
  app.use("/api/payments", paymentRoutes);
  app.use("/api/admin", adminRoutes);
  app.get("/api/search", (req, res) => {
    const qs = new URLSearchParams(req.query as Record<string, string>).toString();
    res.redirect(307, `/api/auctions?${qs}`);
  });

  app.use(errorHandler);
  return app;
}
