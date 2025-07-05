import { Skeleton } from "../ui/skeleton";

// Loading placeholder
export function RepositoryCardSkeleton() {
  return (
    <div className="flex flex-col items-start py-3 border-b border-border w-full gap-2">
      <Skeleton className="w-40 h-6" />
      <Skeleton className="w-140 h-4" />
    </div>
  );
}
