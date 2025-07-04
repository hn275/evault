import { Avatar, Box, Stack, Typography } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";
import { Breadcrumbs } from "../../components/common/Breadcrumbs";
import { useUser } from "../../hooks/auth";
import { useRepository } from "../../hooks/repository";
import { RepositoryList } from "../../components/dashboard/RepositoryList";
import { LoaderWithText } from "../../components/common/LoaderWithText";

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
    <Box display="flex" flexDirection="column" gap={1}>
      {user && repos ? (
        <>
          <Breadcrumbs paths={[{ display: "Dashboard", href: "/dashboard" }]} />

          <Box display="flex" alignItems="center" gap={2}>
            <Avatar src={user.avatar_url} alt={user.name} />
            <Stack>
              <Typography
                fontWeight={500}
                fontSize="1.2em"
                color="text.primary"
              >
                {user.name}
              </Typography>
              <Typography
                fontWeight={400}
                fontSize="0.8em"
                color="text.secondary"
              >
                {user.login}
              </Typography>
            </Stack>
            {/* <p>Email: {user.email}</p> */}
          </Box>

          <section>
            {repos ? (
              <RepositoryList repositories={repos} />
            ) : (
              <LoaderWithText text="Fetching Repos..." />
            )}
          </section>
        </>
      ) : (
        <LoaderWithText text="Loading..." />
      )}
    </Box>
  );
}
