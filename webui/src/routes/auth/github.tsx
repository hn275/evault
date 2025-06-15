import { createFileRoute } from "@tanstack/react-router";
import { z } from "zod/v4";
import { paramParser } from "../../utils/zod/gitHubParams";
import { useAuthGithub } from "../../hooks/auth";

type SearchParam = z.infer<typeof paramParser>;

export const Route = createFileRoute("/auth/github")({
  validateSearch: (s: Record<string, unknown>): SearchParam =>
    paramParser.parse(s),
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
