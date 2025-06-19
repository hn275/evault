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
    // NOTE: can't do `fetch` here because the server is redirecting the request
    // to the OAuth provider (GitHub), with `fetch`, browser blocks the redirect.
    // this way the browser itself is making the `GET` request to be redirected.
    window.location.href = "/api/github/auth?device_type=web";
  }

  return { signInRedirect };
}
