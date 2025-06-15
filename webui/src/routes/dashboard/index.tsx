import { Avatar, Box, Stack, Typography } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";
import { Breadcrumbs } from "../../components/common/Breadcrumbs";
import { useUser } from "../../hooks/auth";
import { RepositoryCard } from "../../components/dashboard/RepositoryCard";
import { useRepository } from "../../hooks/repository";

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
                  <RepositoryCard key={repo.id} repo={repo} />
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
