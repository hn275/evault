import {
  createFileRoute,
  useSearch,
  useNavigate,
} from "@tanstack/react-router";
import { useState, useEffect } from "react";

type DeviceType = "web" | "cli";

type AuthGitHubSearchParam = {
  session_id: string;
  device_type: DeviceType;
  code: string;
  state: string;
};

export const Route = createFileRoute("/auth/github")({
  validateSearch: (s: Record<string, string>): AuthGitHubSearchParam => {
    return {
      session_id: s.session_id,
      device_type: s.device_type as DeviceType,
      code: s.code,
      state: s.state,
    };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const f = useAuthGithub();
  return f.loading ? (
    <>Authenticating...</>
  ) : f.error !== null ? (
    <> {f.error}</>
  ) : (
    <>Authenticated, you can now close this window.</>
  );
}

function useAuthGithub() {
  const param = useSearch({ from: "/auth/github" });
  const nav = useNavigate();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sessionId = param["session_id"];
    const oauthCode = param["code"];
    const oauthState = param["state"];
    const deviceType = param["device_type"];

    if (!sessionId || !oauthCode || !oauthState || !deviceType) {
      throw new Error("Invalid params.");
    }

    (async () => {
      const p = new URLSearchParams({
        session_id: sessionId,
        code: oauthCode,
        state: oauthState,
        device_type: deviceType,
      });

      try {
        await fetch(`/api/auth/token?${p.toString()}`);

        if (deviceType === "web") {
          nav({ to: "/dashboard" });
        }
      } catch (e) {
        setError("Something went wrong.");
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return { loading, error };
}
