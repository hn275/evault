import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/auth/")({
  head: () => ({
    meta: [
      {
        title: "Authenticating | Evault",
      },
    ],
  }),
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/auth/"!</div>;
}
