"use client";

import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import { API_URL } from "./api";

let shared: Socket | null = null;
const joinedAuctions = new Set<string>();

function authToken() {
  if (typeof window === "undefined") return undefined;
  return localStorage.getItem("token") || undefined;
}

export function getSocket() {
  if (typeof window === "undefined") return null;
  if (!shared) {
    shared = io(API_URL, {
      withCredentials: true,
      autoConnect: true,
      auth: { token: authToken() },
    });
    shared.on("connect", () => {
      for (const id of joinedAuctions) {
        shared?.emit("auction:join", id);
      }
    });
  } else {
    shared.auth = { token: authToken() };
  }
  return shared;
}

export function joinAuctionRoom(auctionId: string) {
  const s = getSocket();
  if (!auctionId) return;
  joinedAuctions.add(auctionId);
  s?.emit("auction:join", auctionId);
}

export function leaveAuctionRoom(auctionId: string) {
  const s = getSocket();
  if (!auctionId) return;
  joinedAuctions.delete(auctionId);
  s?.emit("auction:leave", auctionId);
}

export function useSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  useEffect(() => {
    const s = getSocket();
    setSocket(s);
  }, []);
  return socket;
}
