import { createFileRoute } from "@tanstack/react-router";
import { Breadcrumbs } from "../../components/common/Breadcrumbs";
import { useUser } from "../../hooks/auth";
import { useRepository } from "../../hooks/repository";
import { RepositoryList } from "../../components/dashboard/RepositoryList";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { RepositoryCardSkeleton } from "@/components/dashboard/RepositoryCardSkeleton";
import { Skeleton } from "@/components/ui/skeleton";

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
  const { user } = useUser();
  const { repos } = useRepository();

  return (
    <div className="flex flex-col gap-1">
      <Breadcrumbs paths={[{ display: "Dashboard", href: "/dashboard" }]} />
      {user && repos ? (
        <>
          <div className="flex items-center gap-2">
            <Avatar>
              <AvatarImage src={user.avatar_url} />
              <AvatarFallback>{user.name?.charAt(0)}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <p className="font-medium text-lg">{user.name}</p>
              <p className="text-sm text-muted-foreground">{user.login}</p>
            </div>
            {/* <p>Email: {user.email}</p> */}
          </div>

          <section>
            {repos ? (
              <RepositoryList repositories={repos} />
            ) : (
              [...Array(10)].map((_, index) => (
                <RepositoryCardSkeleton key={index} />
              ))
            )}
          </section>
        </>
      ) : (
        <div className="flex items-center space-x-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-4 w-[250px]" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
        </div>
      )}
    </div>
  );
}
