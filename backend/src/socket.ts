import { Server as HttpServer } from "http";
import { Server, Socket } from "socket.io";
import jwt from "jsonwebtoken";
import { getCorsOrigins } from "./lib/corsOrigins";

let io: Server | null = null;

function parseCookieToken(cookieHeader?: string) {
  if (!cookieHeader) return undefined;
  const match = cookieHeader.match(/(?:^|;\s*)token=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : undefined;
}

function socketUserId(socket: Socket): string | null {
  const secret = process.env.JWT_SECRET?.trim();
  if (!secret || secret.length < 16) {
    if (process.env.NODE_ENV === "production") return null;
  }
  const jwtSecret = secret && secret.length >= 16 ? secret : "bid-on-dev-secret";
  const fromAuth =
    typeof socket.handshake.auth?.token === "string"
      ? socket.handshake.auth.token
      : undefined;
  const fromHeader = socket.handshake.headers.authorization?.startsWith("Bearer ")
    ? socket.handshake.headers.authorization.slice(7)
    : undefined;
  const token =
    fromAuth || fromHeader || parseCookieToken(socket.handshake.headers.cookie);
  if (!token) return null;
  try {
    const payload = jwt.verify(token, jwtSecret) as { id?: string };
    return payload.id || null;
  } catch {
    return null;
  }
}

export function initSocket(httpServer: HttpServer) {
  io = new Server(httpServer, {
    cors: {
      origin: getCorsOrigins(),
      credentials: true,
    },
  });

  io.on("connection", (socket: Socket) => {
    const authedUserId = socketUserId(socket);
    if (authedUserId) {
      socket.join(`user:${authedUserId}`);
    }

    socket.on("auction:join", (auctionId: string) => {
      if (typeof auctionId === "string" && auctionId.length > 0) {
        socket.join(`auction:${auctionId}`);
      }
    });
    socket.on("auction:leave", (auctionId: string) => {
      if (typeof auctionId === "string" && auctionId.length > 0) {
        socket.leave(`auction:${auctionId}`);
      }
    });
    // Legacy client event — only join the authenticated user's room.
    socket.on("user:join", (userId: string) => {
      if (authedUserId && userId === authedUserId) {
        socket.join(`user:${authedUserId}`);
      }
    });
  });

  return io;
}

export function getIO() {
  if (!io) throw new Error("Socket.IO not initialized");
  return io;
}

export function emitBidUpdate(auctionId: string, payload: unknown) {
  getIO().to(`auction:${auctionId}`).emit("bid:new", payload);
}

export function emitAuctionEnded(auctionId: string, payload: unknown) {
  getIO().to(`auction:${auctionId}`).emit("auction:ended", payload);
}

export function emitNotification(userId: string, payload: unknown) {
  getIO().to(`user:${userId}`).emit("notification:new", payload);
}
