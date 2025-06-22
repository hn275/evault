import { Box } from "@mui/material";
import { RepositoryCard } from "./RepositoryCard";
import type { Repository } from "../../types/Repository";

export function RepositoryList({
  repositories,
}: {
  repositories: Repository[];
}) {
  return (
    <Box>
      {repositories.map((repo) => (
        <RepositoryCard repo={repo} key={repo.id} />
      ))}
    </Box>
  );
}
