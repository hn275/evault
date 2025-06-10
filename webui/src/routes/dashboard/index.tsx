import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState, useEffect } from "react";

export const Route = createFileRoute("/dashboard/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { user } = useUser();
  const { repos } = useRepository();

  return (
    <>
      Dash
      {user ? (
        <>
          <section>
            <p>Username: {user.name}</p>
            <p>Login: {user.login}</p>
            <p>User Type: {user.type}</p>
            <p>Email: {user.email}</p>
            <img src={user.avatar_url} />
          </section>

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
      if (r.status === 403) nav({ to: "/" });

      const d = (await r.json()) as User;
      setUser(d);
    })();
  }, []);

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
      if (r.status === 403) nav({ to: "/" });
      const data = await r.json();
      setRepos(data);
    })();
  }, []);

  return {
    repos,
  };
}
