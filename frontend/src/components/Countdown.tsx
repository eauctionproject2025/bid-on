"use client";

import { useEffect, useRef, useState } from "react";

export function Countdown({
  endsAt,
  onEnded,
}: {
  endsAt: string;
  onEnded?: () => void;
}) {
  const [label, setLabel] = useState("—");
  const [urgent, setUrgent] = useState(false);
  const endedFired = useRef(false);

  useEffect(() => {
    endedFired.current = false;
    const tick = () => {
      const diff = new Date(endsAt).getTime() - Date.now();
      if (diff <= 0) {
        setLabel("Ended");
        setUrgent(false);
        if (!endedFired.current) {
          endedFired.current = true;
          onEnded?.();
        }
        return;
      }
      setUrgent(diff < 60 * 60 * 1000);
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      if (h > 48) {
        const d = Math.floor(h / 24);
        setLabel(`${d}d ${h % 24}h left`);
      } else {
        setLabel(
          `${h.toString().padStart(2, "0")}:${m
            .toString()
            .padStart(2, "0")}:${s.toString().padStart(2, "0")}`
        );
      }
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [endsAt, onEnded]);

  return (
    <span
      className={`font-mono tracking-tight ${urgent ? "countdown-urgent" : ""}`}
    >
      {label}
    </span>
  );
}
