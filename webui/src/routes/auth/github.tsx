import { createFileRoute, Navigate } from "@tanstack/react-router";
import {
  paramParser,
  type GitHubOAuthSearchParamResult,
} from "../../utils/zod/gitHubParams";
import { useAuthGithub } from "../../hooks/auth";
import { CircularProgress, Link, Stack, Typography } from "@mui/material";
import { AnimatePresence, motion } from "motion/react";
import { Link as RouterLink } from "@tanstack/react-router";
import { useLoadingText } from "../../hooks/loadingText";

const TEXT_CHANGE_INTERVAL = 3000; // milliseconds
const loadingTexts = [
  "Authenticating with secure provider...",
  "Verifying your identity...",
  "Syncing your security credentials...",
  "Confirming sharing privileges...",
  "Checking vault sharing authorization...",
];

export const Route = createFileRoute("/auth/github")({
  validateSearch: (s: Record<string, unknown>): GitHubOAuthSearchParamResult =>
    paramParser.safeParse(s),
  component: RouteComponent,
});

function RouteComponent() {
  const f = useAuthGithub();

  switch (f.status) {
    case "pending":
      return <LoadingState />;
    case "error":
      return <ErrorState />;
    default:
      return <Navigate to="/dashboard" />;
  }
}

function ErrorState() {
  return (
    <Stack mt="30vh" mx="auto" width="max-content" alignItems="center" gap={1}>
      <Typography variant="h4">Authentication Failed</Typography>
      <Link component={RouterLink} to="/">
        Go back home.
      </Link>
    </Stack>
  );
}

function LoadingState() {
  const { index } = useLoadingText(TEXT_CHANGE_INTERVAL, loadingTexts);

  return (
    <Stack
      gap={4}
      mt="30vh"
      justifyItems="center"
      alignItems="center"
      mx="auto"
    >
      <Typography variant="h4" color="text.primary">
        Authenticating with GitHub
      </Typography>

      <Stack justifyItems="center" alignItems="center" gap={2}>
        <CircularProgress />
        <AnimatePresence mode="wait">
          {loadingTexts.map((text, idx) => {
            return index === idx ? (
              <motion.div
                key={`text-key-${idx}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
              >
                <Typography variant="body1" color="text.secondary">
                  {text}
                </Typography>
              </motion.div>
            ) : null;
          })}
        </AnimatePresence>
      </Stack>
    </Stack>
  );
}
