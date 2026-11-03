"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAuth } from "@/lib/auth";
import { useResendOtp, useVerifyOtp } from "@/hooks/queries";
import { resendVerifySchema, ResendVerifyValues } from "@/lib/schemas";
import { toastFromError, toastSuccess, toastValidationErrors } from "@/lib/toast";

function VerifyInner() {
  const params = useSearchParams();
  const router = useRouter();
  const { setSession } = useAuth();
  const verifyMutation = useVerifyOtp();
  const resendMutation = useResendOtp();
  const token = params.get("token") || "";
  const [status, setStatus] = useState<"idle" | "verifying" | "error">(
    token ? "verifying" : "idle"
  );
  const [errorMsg, setErrorMsg] = useState("");
  const [verifyLink, setVerifyLink] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const tried = useRef(false);

  useEffect(() => {
    const stored = sessionStorage.getItem("bidon-verify-url");
    if (stored) {
      setVerifyLink(stored);
      sessionStorage.removeItem("bidon-verify-url");
    }
    const storedPreview = sessionStorage.getItem("bidon-email-preview");
    if (storedPreview) {
      setPreviewUrl(storedPreview);
      sessionStorage.removeItem("bidon-email-preview");
    }
  }, []);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<ResendVerifyValues>({
    resolver: zodResolver(resendVerifySchema),
    defaultValues: { email: params.get("email") || "" },
  });

  useEffect(() => {
    if (!token || tried.current) return;
    const gateKey = `verified:${token}`;
    if (sessionStorage.getItem(gateKey) === "1") {
      router.replace("/dashboard");
      return;
    }
    tried.current = true;

    (async () => {
      try {
        const data = await verifyMutation.mutateAsync({ token });
        sessionStorage.setItem(gateKey, "1");
        setSession(data.token, data.user);
        toastSuccess("Email verified successfully");
        router.replace("/dashboard");
      } catch (err) {
        if (sessionStorage.getItem(gateKey) === "1") {
          router.replace("/dashboard");
          return;
        }
        const msg = toastFromError(err, "Verification failed");
        setErrorMsg(msg);
        setStatus("error");
      }
    })();
    // Intentionally run once when token is present
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const onResend = handleSubmit(
    async (values) => {
      try {
        const data = await resendMutation.mutateAsync(values.email);
        toastSuccess(data.message);
        if (data.verifyUrl) setVerifyLink(data.verifyUrl);
        if (data.emailPreviewUrl) setPreviewUrl(data.emailPreviewUrl);
      } catch (err) {
        const msg = toastFromError(err, "Resend failed");
        setError("root", { message: msg });
      }
    },
    (formErrors) => toastValidationErrors(formErrors)
  );

  if (token && status === "verifying") {
    return (
      <div className="mx-auto max-w-md px-4 py-16">
        <Card>
          <CardHeader>
            <CardTitle className="font-[family-name:var(--font-display)] text-4xl">
              Verifying…
            </CardTitle>
            <CardDescription>
              Confirming your email. This only takes a moment.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  if (token && status === "error") {
    return (
      <div className="mx-auto max-w-md px-4 py-16">
        <Card>
          <CardHeader>
            <CardTitle className="font-[family-name:var(--font-display)] text-4xl">
              Link invalid
            </CardTitle>
            <CardDescription>
              {errorMsg || "This verification link is invalid or expired."}
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <Link href="/auth/verify" className="w-full">
              <Button className="w-full" variant="outline">
                Request a new link
              </Button>
            </Link>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-md px-4 py-16">
      <Card>
        <CardHeader>
          <CardTitle className="font-[family-name:var(--font-display)] text-4xl">
            Verify your account
          </CardTitle>
          <CardDescription>
            {verifyLink
              ? "Email delivery is unavailable right now. Open the verification link below to activate your account."
              : "We sent a verification link to your inbox. Open it to activate your account. If it did not arrive, request a new one below."}
          </CardDescription>
        </CardHeader>
        <form onSubmit={onResend}>
          <CardContent className="space-y-4">
            {verifyLink && (
              <div className="space-y-3 rounded-md border border-amber-300 bg-amber-50 p-3 dark:border-amber-700 dark:bg-amber-950/40">
                <p className="text-sm font-medium">
                  Instant verification (email not delivered)
                </p>
                <a href={verifyLink} className="block w-full">
                  <Button type="button" className="w-full">
                    Open verification link
                  </Button>
                </a>
                <p className="break-all text-xs text-muted-foreground">
                  {verifyLink}
                </p>
              </div>
            )}
            {previewUrl && (
              <p className="text-sm">
                Test inbox preview:{" "}
                <a
                  href={previewUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary underline"
                >
                  open Ethereal message
                </a>
              </p>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" {...register("email")} />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email.message}</p>
              )}
            </div>
            {errors.root && (
              <p className="text-sm text-destructive">{errors.root.message}</p>
            )}
          </CardContent>
          <CardFooter className="flex flex-col gap-3">
            <Button
              type="submit"
              className="w-full"
              variant={verifyLink ? "outline" : "default"}
              disabled={resendMutation.isPending}
            >
              {resendMutation.isPending
                ? "Sending…"
                : "Resend verification email"}
            </Button>
            <p className="text-sm text-muted-foreground">
              <Link
                href="/auth/login"
                className="text-primary underline-offset-4 hover:underline"
              >
                Back to log in
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}

export default function VerifyPage() {
  return (
    <Suspense>
      <VerifyInner />
    </Suspense>
  );
}
