import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import type { Repository } from "../types/Repository";
import { getUserRepositories } from "../services/repository";

export function useRepository() {
  const [repos, setRepos] = useState<Repository[] | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    (async function () {
      const data = await getUserRepositories();
      setRepos(data);
    })();
  }, [nav]);

  return {
    repos,
  };
}