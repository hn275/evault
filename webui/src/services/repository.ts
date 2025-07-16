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
      let statusOk = status >= HttpStatusCode._200_OK;
      statusOk ||= status < HttpStatusCode._300_MULTIPLE_CHOICES;
      statusOk ||= status === HttpStatusCode._404_NOT_FOUND;
      return statusOk;
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
