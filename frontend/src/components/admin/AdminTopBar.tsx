"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { ExternalLink, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth";
import { useThemeStore } from "@/stores/theme-store";
import { toastError, toastSuccess } from "@/lib/toast";

async function exportCsv() {
  const token = localStorage.getItem("token");
  const { API_URL } = await import("@/lib/api");
  const res = await fetch(`${API_URL}/api/admin/reports/csv`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error("Export failed");
  }
  const csv = await res.text();
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "auctions-report.csv";
  a.click();
  URL.revokeObjectURL(url);
}

export function AdminTopBar() {
  const router = useRouter();
  const user = useAuth((s) => s.user);
  const logout = useAuth((s) => s.logout);
  const theme = useThemeStore((s) => s.theme);
  const toggleTheme = useThemeStore((s) => s.toggleTheme);

  return (
    <header className="flex h-12 shrink-0 items-center justify-between gap-4 border-b border-border bg-background px-4">
      <p className="text-sm font-medium tracking-tight">Operations</p>
      <div className="flex items-center gap-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            void exportCsv().catch(() => toastError("CSV export failed"));
          }}
        >
          Export CSV
        </Button>
        <Button
          type="button"
          variant="ghost"
          size="icon-sm"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {theme === "light" ? <Moon /> : <Sun />}
        </Button>
        {user ? (
          <span className="hidden text-xs text-muted-foreground sm:inline">
            {user.email}
          </span>
        ) : null}
        <Button
          variant="ghost"
          size="sm"
          onClick={async () => {
            await logout();
            toastSuccess("Logged out");
            router.push("/auth/login");
          }}
        >
          Log out
        </Button>
        <Link href="/">
          <Button variant="outline" size="sm">
            Exit to site
            <ExternalLink className="size-3.5" />
          </Button>
        </Link>
      </div>
    </header>
  );
}
