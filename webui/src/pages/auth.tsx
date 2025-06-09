import { useEffect, useState } from "react";
import { useSearchParams, redirect, useNavigate } from "react-router-dom";
// path /auth
export function Auth() {
  useAuth();

  return <>Redirecting to GitHub OAuth...</>;
}

function useAuth() {
  const [param] = useSearchParams();
  useEffect(() => {
    const sessionId = param.get("session_id");
    (async () => {
      const r = await fetch(
        // TODO: change the API url, pull from env
        `http://localhost:8000/api/auth/url?session_id=${sessionId}`,
      );
      window.location.href = await r.text();
    })();
  }, []);
}

// path /auth/github
export function AuthGithub() {
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
  const [param] = useSearchParams();
  const nav = useNavigate();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sessionId = param.get("session_id");
    const oauthCode = param.get("code");
    const oauthState = param.get("state");
    const deviceType = param.get("device_type");

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
        const r = await fetch(`/api/auth/token?${p.toString()}`);

        if (deviceType === "web") {
          nav("/dashboard");
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
