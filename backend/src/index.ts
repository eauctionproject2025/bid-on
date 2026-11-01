import "dotenv/config";
import http from "http";
import { createApp } from "./app";
import { initSocket } from "./socket";
import { startAuctionEnder } from "./jobs/auctionEnder";

const port = Number(process.env.PORT || 4000);
const app = createApp();
const server = http.createServer(app);

initSocket(server);
startAuctionEnder(30_000);

server.listen(port, "0.0.0.0", () => {
  console.log(`Bid On API listening on http://0.0.0.0:${port}`);
});
