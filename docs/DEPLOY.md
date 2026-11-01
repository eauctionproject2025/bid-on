# Deploy Bid On — Vercel (frontend) + Render (backend)

This guide deploys the Next.js app to **Vercel** and the Express/Prisma API to **Render**, with managed PostgreSQL.

The Blueprint is [`render.yaml`](../render.yaml) at the repository root. Render creates:

| Piece | Host | Notes |
|-------|------|--------|
| Frontend | Vercel | Root directory `frontend` |
| Backend API | Render web service `bid-on-api` | Root directory `backend`, region Singapore |
| Database | Render Postgres `bid-on-db` | PostgreSQL 16, private network only |

Wire the two apps together:

- Vercel: `NEXT_PUBLIC_API_URL=https://bid-on-api.onrender.com` (no trailing slash; use the real host Render assigns)
- Render: `FRONTEND_URL=https://<your-vercel-app>.vercel.app` (no trailing slash)

## Prerequisites

- This repo on GitHub (`master`)
- [Vercel](https://vercel.com) account
- [Render](https://render.com) account
- The Blueprint generates `JWT_SECRET`. You still set `FRONTEND_URL` when Render asks.

Free Render limits (fine for a demo, not for production):

- The web service sleeps after about 15 minutes with no traffic. The first request after sleep can take up to a minute, and the auction-end job pauses while the service is asleep.
- Free Postgres expires 30 days after creation (then a 14-day upgrade window). One free database per workspace. No backups.
- Uploaded images live on the instance disk (`UPLOAD_DIR=uploads`) and are wiped on the next deploy. A persistent disk needs a paid web service.

## 1. Deploy the API and database on Render

1. Push `master` so GitHub has `render.yaml`.
2. In the [Render Dashboard](https://dashboard.render.com), choose **New → Blueprint**.
3. Connect GitHub and select this repository. Render reads `render.yaml`.
4. When prompted, set `FRONTEND_URL` to the Vercel origin if you already have one. If the frontend is not deployed yet, use a placeholder such as `https://bid-on.vercel.app` and update it after the Vercel deploy.
5. Apply the Blueprint. Render creates `bid-on-db` and `bid-on-api` in **Singapore** and deploys the API.

Build and start (from the Blueprint):

- Build: `npm install --include=dev && npm run build` (`prisma` and `typescript` are devDependencies)
- Start: `npm start` (`prisma migrate deploy`, then `node dist/index.js`)
- Health check: `/api/health`
- `DATABASE_URL` is the internal Postgres URL. Do not paste it into Git.

6. Open the service URL Render shows, then `https://<render-host>/api/health`. Expect `{ "ok": true, "service": "bid-on" }`.
7. API docs: `https://<render-host>/api/docs`
8. Optional demo data (once): open the service **Shell** and run `npm run db:seed`.

`PORT` is set by Render. The process listens on `0.0.0.0`.

### Stripe webhooks (if using Stripe)

In the [Stripe Dashboard](https://dashboard.stripe.com/test/webhooks) (test mode), add:

`https://<render-host>/api/payments/webhook`

Copy the signing secret into `STRIPE_WEBHOOK_SECRET` on the API service (Environment), add `STRIPE_SECRET_KEY` the same way, and redeploy. Leave both empty to keep simulated payments.

## 2. Deploy the frontend on Vercel

1. [Import the GitHub repo](https://vercel.com/new) into Vercel.
2. Configure the project:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - Leave build/output defaults (`next build` / `.next`)
3. Environment variables → Production (and Preview if you want):

| Variable | Value |
|----------|--------|
| `NEXT_PUBLIC_API_URL` | `https://<render-host>` (no trailing slash) |

4. Deploy. Note the production URL (`https://….vercel.app`).
5. On Render, set `FRONTEND_URL` to that exact origin (scheme + host, no path, no trailing slash) and redeploy the API so CORS and Socket.IO allow the frontend.

## 3. Smoke test

- [ ] `GET /api/health` on Render returns OK
- [ ] Register / login from the Vercel site
- [ ] Live auction bids update (Socket.IO). Wake the free API first if it has been idle.
- [ ] Stripe checkout (if configured) completes and webhook/session-status marks paid

## Troubleshooting

### Build fails on `tsc` or `prisma`

The build command must install devDependencies:

`npm install --include=dev && npm run build`

Root directory must be `backend`, not the repository root.

### Database connection refused during migrate

`bid-on-api` and `bid-on-db` must be in the same region (Singapore in `render.yaml`). `DATABASE_URL` must be the **internal** connection string from `fromDatabase`, not the external URL.

### CORS or Socket.IO fails

`FRONTEND_URL` on Render must exactly match the Vercel origin, then redeploy the API.

### Free database expired

Upgrade `bid-on-db` to a paid plan before the 14-day grace period ends, or the data is deleted.

## Custom domains (optional)

1. Attach a custom domain on Vercel for the frontend.
2. Attach a custom domain on Render for the API.
3. Update `FRONTEND_URL` and `NEXT_PUBLIC_API_URL` to the new origins and redeploy each side.
4. Update the Stripe webhook URL if you use Stripe.

## Local vs production env files

| App | Local file | Example |
|-----|------------|---------|
| Backend | `backend/.env` | [`backend/.env.example`](../backend/.env.example) |
| Frontend | `frontend/.env.local` | [`frontend/.env.example`](../frontend/.env.example) |

Never commit real secrets. Production secrets live only in the Vercel and Render dashboards.
