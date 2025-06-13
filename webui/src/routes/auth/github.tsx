import {
  createFileRoute,
  useSearch,
  useNavigate,
} from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { z } from "zod/v4";

const paramParser = z.object({
  session_id: z.string(),
  device_type: z.enum(["web", "cli"]),
  code: z.string(),
  state: z.string(),
});

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

function useAuthGithub() {
  const param = useSearch({ from: "/auth/github" });
  const nav = useNavigate();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const { data: searchParam, error: searchParamError } =
      paramParser.safeParse(param);

    if (searchParamError) {
      setError("Invalid authentication parameters.");
      console.error(searchParamError.message);
      setLoading(false);
      return;
    }

    const p = new URLSearchParams(searchParam);

    (async () => {
      try {
        await fetch(`/api/auth/token?${p.toString()}`);

        if (searchParam.device_type === "web") {
          nav({ to: "/dashboard" });
        }
      } catch (e) {
        setError("Something went wrong.");
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, [nav, param]);

  return { loading, error };
}
