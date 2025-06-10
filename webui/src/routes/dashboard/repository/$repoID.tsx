import { createFileRoute, useLoaderData } from "@tanstack/react-router";
import { useEffect } from "react";

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  component: RouteComponent,
  loader: async ({ params }) => fetchRepoData(parseInt(params.repoID)),
});

type Repository = {
  id: number;
};

type ServerError = number; // http status code

async function fetchRepoData(
  repoID: number,
): Promise<Repository | ServerError | null> {
  const r = await fetch(`/api/dashboard/repository/${repoID}`);
  switch (r.status) {
    case 200:
      return { id: repoID };
    case 404:
      return null;
    default:
      return r.status;
  }
}

function RouteComponent() {
  const repo = useLoaderData({ from: "/dashboard/repository/$repoID" });
  useEffect(() => console.log(repo), [repo]);

  return (
    <>
      {repo === null ? (
        <>
          <button>Create new vault</button>
        </>
      ) : typeof repo === "number" ? (
        <>{repo}</>
      ) : (
        <>
          <section>Hello {` /dashboard/repository/${repo!.id}`}!</section>
        </>
      )}
      <div></div>
    </>
  );
}
