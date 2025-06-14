import {
  createFileRoute,
  Link,
  useLoaderData,
  useSearch,
} from "@tanstack/react-router";
import { Breadcrumbs } from "../../../components/Breadcrumbs";
import type { Status } from "../../../types/API";
import { NewVault } from "../../../components/dashboard/repository/NewVaultForm";
import { useState } from "react";
import { Button } from "@mui/material";
import { useNotifications } from "@toolpad/core/useNotifications";

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

// TODO:This will need to be moved to a service file during refactor
async function fetchRepoData(
  repoID: number,
  repoFullName: string,
): Promise<Status> {
  const r = await fetch(
    `/api/dashboard/repository/${repoID}?repo=${repoFullName}`,
  );
  return { id: repoID, status: r.status };
}

function RouteComponent() {
  const notifications = useNotifications();
  const repoID = useLoaderData({ from: "/dashboard/repository/$repoID" });
  const { repo: repoFullName } = useSearch({
    from: "/dashboard/repository/$repoID",
  });

  const [newVaultDialogOpen, setNewVaultDialogOpen] = useState(
    repoID.status === 404,
  );

  if (repoID.status === 403) {
    notifications.show(
      "You are not authorized to create a vault for this repository.",
      {
        severity: "error",
        autoHideDuration: 3000,
      },
    );
  }

  // TODO: Breadcrumbs should be a common layout route
  const breadcrumbs = [
    { display: "Dashboard", href: "/dashboard" },
    { display: repoFullName, href: `https://github.com/${repoFullName}` },
  ];

  return (
    <>
      <Breadcrumbs paths={breadcrumbs} />
      <NewVault
        repoID={repoID.id}
        repoFullName={repoFullName}
        open={newVaultDialogOpen}
        setDialogOpen={setNewVaultDialogOpen}
      />
      {repoID.status === 440 ? (
        <>
          Session expired. Go back&nbsp;
          <Link to="/">Home.</Link>
        </>
      ) : repoID.status === 403 ? (
        <>You are not authorized to create a vault for this repository.</>
      ) : repoID.status === 200 ? (
        <>Vault found.</>
      ) : repoID.status === 404 ? (
        <>
          <Button
            variant="contained"
            onClick={() => setNewVaultDialogOpen(true)}
          >
            Create Vault
          </Button>
        </>
      ) : (
        <>Something went wrong.</>
      )}
    </>
  );
}
