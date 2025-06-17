import type { User } from "../types/User";
import { httpClient } from "../utils/axios";

// Fetch the user's information from the API
export async function getUser(): Promise<User> {
  const r = await httpClient.get("/api/dashboard/user", {
    transformResponse: (data) => {
      // TODO: adding zod type validation
      return data;
    },
  });
  return r.data;
}

// Exchange the GitHub authentication
export async function getGitHubAuth(p: URLSearchParams) {
  return httpClient.get(`/api/auth/token?${p.toString()}`);
}
