import type { Repository } from "../../types/Repository";
import { Link } from "@tanstack/react-router";
import { Badge } from "../ui/badge";
import { Globe, Lock } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent } from "../ui/card";

export function RepositoryCard({ repo }: { repo: Repository }) {
  return (
    <Card className="flex justify-between items-start py-3 border-b border-border">
      <CardContent className="flex flex-row justify-between w-full">
        <div className="flex-grow">
          <div className="flex items-center gap-1 mb-1">
            <Link
              to="/dashboard/repository/$repoID"
              params={{ repoID: `${repo.id}` }}
              search={{ repo: repo.full_name }}
            >
              <p className="text-lg font-semibold text-primary hover:underline">
                {repo.full_name}
              </p>
            </Link>
            <Badge
              variant={repo.private ? "destructive" : "default"}
              className="text-xs bg-background border border-border py-1 h-5"
            >
              {repo.private ? (
                <Lock className="w-4 h-4 text-muted-foreground" />
              ) : (
                <Globe className="w-4 h-4 text-muted-foreground" />
              )}
            </Badge>
          </div>
          {repo.description && (
            <p className="text-sm text-muted-foreground mb-2">
              {repo.description}
            </p>
          )}
        </div>

        <div className="flex items-center justify-center gap-1 ml-2 min-w-[112px]">
          <Link
            to="/dashboard/repository/$repoID"
            params={{ repoID: `${repo.id}` }}
            search={{ repo: repo.full_name }}
          >
            <Button variant="default" size="sm">
              View Vault
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
