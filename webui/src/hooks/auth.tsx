import { useEffect, useState } from "react";
import { useNavigate, useSearch } from "@tanstack/react-router";
import type { User } from "../types/User";
import { getGitHubAuth, getUser } from "../services/auth";
import { useQuery } from "@tanstack/react-query";
import { httpClient } from "../utils/axios";

export function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    (async function () {
      const d = await getUser();
      setUser(d);
    })();
  }, [nav]);

  return { user };
}

export function useAuthGithub() {
  const params = useSearch({ from: "/auth/github" });
  const nav = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const {
    data,
    isPending: loading,
    error: queryError,
    status,
  } = useQuery({
    queryKey: ["githubauth"],

    // NOTE: fine to coerce the type here, since the prop `enabled` will stop
    // the `queryClient` from issuing a request if `params.error` is set.
    queryFn: () => getGitHubAuth(params.data!),
    enabled: params.error === undefined,
    retry: 0,
  });

  useEffect(() => {
    if (params.error) {
      setError("Invalid parameters provided for GitHub authentication.");
      console.error(params.error);
    } else if (status === "success") {
      // setting CSRF token
      const csrfToken = data;
      console.log(csrfToken);
      httpClient.defaults.headers.common["X-CSRF-Token"] = csrfToken;
      nav({ to: "/dashboard" });
    } else if (status === "error") {
      setError("Something went wrong.");
      console.error(queryError);
    }
  }, [nav, status, error, params.error, queryError, data]);

  return { loading, status, error };
}
