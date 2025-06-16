import type { User } from "../types/User";
import type { GitHubOAuthSearchParams } from "../utils/zod/gitHubParams";
import { fetchWithRedirect } from "./common";

// Fetch the user's information from the API
export async function getUser(): Promise<User> {
  const r = await fetchWithRedirect("/api/dashboard/user");
  return (await r.json()) as User;
}

// Exchange the GitHub authentication
export function getGitHubAuth(
  params: GitHubOAuthSearchParams,
): Promise<Response> {
  const p = new URLSearchParams(params);
  return fetch(`/api/auth/token?${p.toString()}`);
}
