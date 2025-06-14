import { Avatar, Box, Stack, Typography } from "@mui/material";
import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Breadcrumbs } from "../../components/Breadcrumbs";

export const Route = createFileRoute("/dashboard/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { user } = useUser();
  const { repos } = useRepository();

  return (
    <>
      <Breadcrumbs paths={[{ display: "Dashboard", href: "/dashboard" }]} />
      {user ? (
        <>
          <Box display="flex" alignItems="center" gap={2}>
            <Avatar src={user.avatar_url} alt={user.name} />
            <Stack>
              <Typography fontWeight={500} fontSize="1.2em">
                {user.name}
              </Typography>
              <Typography fontWeight={400} fontSize="0.8em">
                {user.login}
              </Typography>
            </Stack>
            {/* <p>Email: {user.email}</p> */}
          </Box>

          <section>
            {repos ? (
              <ul>
                {repos.map((repo) => (
                  <li key={repo.id}>
                    <div>{repo.full_name}</div>
                    <a href={repo.html_url} target="_blank">
                      {repo.html_url}
                    </a>
                    <div>Visibility: {repo.private ? "private" : "public"}</div>
                    <div>
                      Description: {repo.description ?? "No description"}
                    </div>
                    <Link
                      to="/dashboard/repository/$repoID"
                      params={{ repoID: `${repo.id}` }}
                      search={{ repo: repo.full_name }}
                    >
                      View secrets
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <>Fetching Repos...</>
            )}
          </section>
        </>
      ) : (
        <>Loading</>
      )}
    </>
  );
}

type User = {
  id: number;
  login: string;
  email: string;
  avatar_url: string;
  name: string;
  type: string;
};

function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    (async function () {
      const r = await fetch(`/api/dashboard/user`);
      if (r.status === 440) nav({ to: "/" });

      const d = (await r.json()) as User;
      setUser(d);
    })();
  }, [nav]);

  return { user };
}

type Repository = {
  id: number;
  full_name: string;
  private: boolean;
  html_url: string;
  description: null | string;
  owner: RepoOwner;
};

type RepoOwner = {
  id: number;
  login: string;
  avatar_url: string;
};

function useRepository() {
  const [repos, setRepos] = useState<Repository[] | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    (async function () {
      const r = await fetch(`/api/dashboard/repositories`);
      if (r.status === 440) nav({ to: "/" });
      const data = await r.json();
      setRepos(data);
    })();
  }, [nav]);

  return {
    repos,
  };
}
