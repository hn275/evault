import {
  createFileRoute,
  Link,
  useLoaderData,
  useSearch,
} from "@tanstack/react-router";
import { Breadcrumbs } from "../../../components/Breadcrumbs";
import type { Status } from "../../../types/API";
import { NewVault } from "../../../components/dashboard/repository/NewVaultForm";

type SearchParams = {
  repo: string;
};

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  component: RouteComponent,
  loader: async ({ params }) => {
    const search = new URLSearchParams(window.location.search);
    const repoFullName = search.get("repo") as string;
    const r = await fetchRepoData(parseInt(params.repoID), repoFullName);
    return r;
  },
  validateSearch: (search: Record<string, unknown>): SearchParams => {
    const repo = search!.repo as string;
    return { repo };
  },
});

async function fetchRepoData(repoID: number, repoFullName: string): Promise<Status> {
  const r = await fetch(`/api/dashboard/repository/${repoID}?repo=${repoFullName}`);
  return { id: repoID, status: r.status };
}

function RouteComponent() {
  const repoID = useLoaderData({ from: "/dashboard/repository/$repoID" });
  const { repo: repoFullName } = useSearch({
    from: "/dashboard/repository/$repoID",
  });

  const breadcrumbs = [
    { display: "Dashboard", href: "/dashboard" },
    { display: repoFullName, href: `https://github.com/${repoFullName}` },
  ];

  return (
    <>
      <Breadcrumbs paths={breadcrumbs} />
      {repoID.status === 440 ? (
        <>
          Session expired. Go back&nbsp;
          <Link to="/">Home.</Link>
        </>
      ) : repoID.status === 200 ? (
        <>Vault found.</>
      ) : repoID.status === 404 ? (
        <>
          <NewVault repoID={repoID.id} repoFullName={repoFullName} />
        </>
      ) : (
        <>Something went wrong.</>
      )}
    </>
  );
}