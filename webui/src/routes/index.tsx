import { Box, Button, Container, CssBaseline, Typography } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      {
        title: "Evault",
      },
    ],
  }),
  component: App,
});

function App() {
  const h = useHome();

  return (
    <>
      <CssBaseline />
      <Box sx={{ backgroundColor: "#0d1117", py: 8 }}>
        <Container maxWidth="md" sx={{ textAlign: "center" }}>
          <Typography
            variant="h1"
            component="h1"
            sx={{ mb: 3, maxWidth: 600, mx: "auto", color: "text.primary" }}
          >
            Manage all your repo secrets in one place
          </Typography>
          <Typography
            variant="body1"
            sx={{
              fontSize: "1.25rem",
              mb: 4,
              maxWidth: 500,
              mx: "auto",
              color: "text.secondary",
            }}
          >
            Store and access your envs in one place, integrated with your GitHub
            access.
          </Typography>
          <Box sx={{ maxWidth: 400, mx: "auto", mb: 3 }}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              sx={{ py: 1.5, fontSize: "1rem", fontWeight: 500 }}
              onClick={h.signInRedirect}
            >
              Login with GitHub
            </Button>
          </Box>
        </Container>
      </Box>
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
