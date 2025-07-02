import {
  createFileRoute,
  Link,
  useLoaderData,
  useSearch,
} from "@tanstack/react-router";
import { Breadcrumbs } from "../../../components/common/Breadcrumbs";
import { NewVault } from "../../../components/dashboard/repository/NewVaultForm";
import { useState } from "react";
import { useNotifications } from "@toolpad/core/useNotifications";
import { getRepositoryByIDWithOwnerValidation } from "../../../services/repository";

type SearchParams = {
  repo: string;
};

// Since we are using the search params to validate repo owner, we need to create a title based on the search params
// This can be updated to the global state to fetch the repository name once that is implemented
const createTitleBasedOnSearchParams = (search: string) => {
  const repo = new URLSearchParams(search).get("repo");
  return repo ? `${repo} | Evault` : "Repository | Evault";
};

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  head: () => ({
    meta: [
      {
        title: createTitleBasedOnSearchParams(window.location.search),
      },
    ],
  }),
  component: RouteComponent,
  loader: async ({ params }) => {
    // TODO: Instead of passing the search params to the loader, we should use a global state to store the repo name
    // and then use that state to fetch the repository
    const search = new URLSearchParams(window.location.search);
    const repoFullName = search.get("repo") as string;
    const r = await getRepositoryByIDWithOwnerValidation(
      parseInt(params.repoID),
      repoFullName,
    );
    return r;
  },
  validateSearch: (search: Record<string, unknown>): SearchParams => {
    const repo = search!.repo as string;
    return { repo };
  },
});

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
          <button
            onClick={() => setNewVaultDialogOpen(true)}
          >
            Create Vault
          </button>
        </>
      ) : (
        <>Something went wrong.</>
      )}
    </>
  );
}
