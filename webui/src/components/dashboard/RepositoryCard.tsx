import type { Repository } from "../../types/Repository";
import { Link } from "@tanstack/react-router";

export function RepositoryCard({ repo }: { repo: Repository }) {
  return (
    <li key={repo.id}>
      <div>{repo.full_name}</div>
      <a href={repo.html_url} target="_blank">
        {repo.html_url}
      </a>
      <div>Visibility: {repo.private ? "private" : "public"}</div>
      <div>Description: {repo.description ?? "No description"}</div>
      <Link
        to="/dashboard/repository/$repoID"
        params={{ repoID: `${repo.id}` }}
        search={{ repo: repo.full_name }}
      >
        View secrets
      </Link>
    </li>
  );
}
