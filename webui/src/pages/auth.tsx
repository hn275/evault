import { useEffect } from 'react';
import { useSearchParams, redirect } from 'react-router-dom';
// path /auth
export function Auth() {
  useAuth();

  return <>Redirecting to GitHub OAuth...</>;
}

function useAuth() {
  const [param] = useSearchParams();
  useEffect(() => {
    const sessionId = param.get('session_id');
    (async () => {
      const r = await fetch(
        // TODO: change the API url, pull from env
        `http://localhost:8000/api/auth/url?session_id=${sessionId}`,
      );
      window.location.href = await r.text();
    })();
  }, []);
}

export function AuthGithub() {
  useAuthGithub();
  return <>Authenticating...</>;
}

function useAuthGithub() {
  const [param] = useSearchParams();
  useEffect(() => {
    const sessionId = param.get('session_id');
    const oauthCode = param.get('code');
    const oauthState = param.get('state');
    const deviceType = param.get('device_type');

    if (!sessionId || !oauthCode || !oauthState || !deviceType) {
      throw new Error('Invalid params.');
    }

    (async () => {
      const p = new URLSearchParams({
        session_id: sessionId,
        code: oauthCode,
        state: oauthState,
        device_type: deviceType,
      });
      const r = await fetch(`/api/auth/token?${p.toString()}`);
      console.log(r.status);
    })();
  }, []);
}
