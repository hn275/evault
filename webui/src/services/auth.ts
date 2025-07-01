import type { User } from "../types/User";
import { httpClient } from "../utils/axios";
import type { GitHubOAuthSearchParams } from "../utils/zod/gitHubParams";

// Fetch the user's information from the API
export async function getUser(): Promise<User> {
  const r = await httpClient.get("/dashboard/user", {
    transformResponse: (data) => {
      // TODO: add zod type validation
      return JSON.parse(data);
    },
  });
  return r.data;
}

// Exchange the GitHub authentication
export async function getGitHubAuth(oauthParams: GitHubOAuthSearchParams) {
  const p = new URLSearchParams(oauthParams);
  return httpClient.get(`/auth/token?${p.toString()}`);
}
