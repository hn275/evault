import { createFileRoute } from "@tanstack/react-router";
import { useRepository } from "../../hooks/repository";
import { RepositoryList } from "../../components/dashboard/RepositoryList";
import { RepositoryCardSkeleton } from "@/components/dashboard/RepositoryCardSkeleton";
import { useBreadcrumbPaths } from "@/hooks/breadcrumbs";

export const Route = createFileRoute("/dashboard/")({
  head: () => ({
    meta: [
      {
        title: "Dashboard | Evault",
      },
    ],
  }),
  component: RouteComponent,
});

function RouteComponent() {
  const { repos } = useRepository();

  useBreadcrumbPaths([{ display: "Dashboard", href: "/dashboard" }], []);

  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center space-x-4">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">Repositories</h1>
        </div>
      </div>
      <section>
        {repos ? (
          <RepositoryList repositories={repos} />
        ) : (
          <div className="flex flex-col gap-1 mt-4">
            <RepositoryCardSkeleton />
          </div>
        )}
      </section>
    </div>
  );
}
