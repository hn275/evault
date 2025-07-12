import { httpClient } from "@/utils/axios";
import type { Status } from "../types/API";
import type { Repository } from "../types/Repository";
import { reposSchema } from "@/lib/validator/repository";

// Fetch the repository by ID with owner validation
export async function getRepositoryByIDWithOwnerValidation(
  repoID: number,
  repoFullName: string,
): Promise<Status> {
  const r = await httpClient.get(`/dashboard/repository/${repoID}`, {
    params: {
      repo: repoFullName,
    },
    validateStatus: (status) => {
      const statusOk = status >= 200 && status < 300;
      return statusOk || status === 404;
    },
  });
  return { id: repoID, status: r.status };
}

// Fetch the user's repositories
export async function getUserRepositories(): Promise<Repository[]> {
  const r = await httpClient.get("/dashboard/repositories");
  return reposSchema.parse(r.data);
}

export async function createNewRepository(
  params: URLSearchParams,
): Promise<Response> {
  return httpClient.post(`/dashboard/repository/new?${params.toString()}`);
}
