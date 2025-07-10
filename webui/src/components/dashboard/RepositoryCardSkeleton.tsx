import { Card, CardContent } from "../ui/card";
import { Skeleton } from "../ui/skeleton";

// Loading placeholder for repository cards
export function RepositoryCardSkeleton() {
  return (
    <Card className="flex justify-between items-start py-3 border-b border-border">
      <CardContent className="flex flex-row justify-between w-full">
        <div className="flex-grow">
          <div className="flex items-center gap-1 mb-1">
            {/* Repository name skeleton */}
            <Skeleton className="h-6 w-48" />
            {/* Badge skeleton */}
            <Skeleton className="h-5 w-12 rounded-full" />
          </div>
          {/* Description skeleton */}
          <Skeleton className="h-4 w-64 mb-2" />
        </div>

        <div className="flex items-center justify-center gap-1 ml-2 min-w-[112px]">
          {/* Button skeleton */}
          <Skeleton className="h-8 w-20 rounded-md" />
        </div>
      </CardContent>
    </Card>
  );
}
