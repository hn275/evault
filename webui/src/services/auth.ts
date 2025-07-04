import type { User } from "../types/User";
import { httpClient } from "../utils/axios";
import { type AxiosPromise } from "axios";
import type { GitHubOAuthSearchParams } from "../utils/zod/gitHubParams";

// Fetch the user's information from the API
export async function getUser(): Promise<User> {
  const r = await httpClient.get("/user");
  return r.data as User;
}

// Exchange the GitHub authentication
export function getGitHubAuth(
  params: GitHubOAuthSearchParams,
): AxiosPromise<string> {
  const p = new URLSearchParams(params);
  return httpClient.get(`/auth/token?${p.toString()}`);
}
