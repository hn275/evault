import { useEffect, useState } from "react";
import { useNavigate, useSearch } from "@tanstack/react-router";
import { paramParser } from "../utils/zod/gitHubParams";
import type { User } from "../types/User";
import { getGitHubAuth, getUser } from "../services/auth";

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
        await getGitHubAuth(p);

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
