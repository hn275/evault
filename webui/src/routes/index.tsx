import { Button } from "@/components/ui/button";
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
    <div className="bg-background pt-[30vh] h-screen">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-3 max-w-[600px] mx-auto text-primary">
          Manage all your repo secrets in one place
        </h1>
        <p className="text-lg mb-4 max-w-[500px] mx-auto text-muted-foreground">
          Store and access your envs in one place, integrated with your GitHub
          access.
        </p>
        <div className="max-w-[400px] mx-auto mb-3">
          <Button
            variant="default"
            size="lg"
            className="w-full"
            onClick={h.signInRedirect}
          >
            Login with GitHub
          </Button>
        </div>
      </div>
    </div>
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
