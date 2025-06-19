import type { Status } from "../types/API";
import type { Repository } from "../types/Repository";
import { fetchWithRedirect } from "./common";

// Fetch the repository by ID with owner validation
export async function getRepositoryByIDWithOwnerValidation(
  repoID: number,
  repoFullName: string,
): Promise<Status> {
  const r = await fetchWithRedirect(
    `/api/github/dashboard/repository/${repoID}?repo=${repoFullName}`,
  );
  return { id: repoID, status: r.status };
}

// Fetch the user's repositories
export async function getUserRepositories(): Promise<Repository[]> {
  const r = await fetchWithRedirect("/api/github/dashboard/repositories");
  return (await r.json()) as Repository[];
}

export async function createNewRepository(
  params: URLSearchParams,
): Promise<Response> {
  return fetchWithRedirect(
    `/api/github/dashboard/repository/new?${params.toString()}`,
    {
      method: "POST",
    },
  );
}
