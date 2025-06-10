import { Button } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  const h = useHome();

  return (
    <>
      <Button variant="contained" onClick={h.signInRedirect}>
        Sign In with GitHub
      </Button>
    </>
  );
}

function useHome() {
  async function signInRedirect() {
    // get session_id
    let r = await fetch(`/api/auth?device_type=web`);
    const url = new URL(await r.text());
    const searchParams = new URLSearchParams(url.search);
    const sessionID = searchParams.get("session_id");

    // get auth url and redirect
    r = await fetch(`/api/auth/url?session_id=${sessionID}`);
    window.location.href = await r.text();
  }

  return { signInRedirect };
}
