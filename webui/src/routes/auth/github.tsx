import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import {
  createFileRoute,
  useSearch,
  useNavigate,
  Link as RouterLink,
} from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { z } from "zod/v4";
import { Link, CircularProgress, Stack, Typography } from "@mui/material";
import { AnimatePresence, motion } from "framer-motion";

const paramParser = z.object({
  session_id: z.string(),
  device_type: z.enum(["web", "cli"]),
  code: z.string(),
  state: z.string(),
});

type SearchParam = z.infer<typeof paramParser>;

export const Route = createFileRoute("/auth/github")({
  validateSearch: (s: Record<string, unknown>): SearchParam =>
    paramParser.parse(s),
  component: RouteComponent,
});

function RouteComponent() {
  const f = useAuthGithub();

  const { index, loadingTexts } = useLoadingText();

  return f.status === "pending" ? (
    <Stack
      gap={4}
      mt="30vh"
      justifyItems="center"
      alignItems="center"
      mx="auto"
    >
      <Typography variant="h4">Authenticating with GitHub</Typography>

      <Stack justifyItems="center" alignItems="center" gap={2}>
        <CircularProgress />
        <AnimatePresence mode="wait">
          {loadingTexts.map((text, idx) => {
            return index === idx ? (
              <motion.div
                key={`text-key-${idx}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <Typography variant="body1">{text}</Typography>
              </motion.div>
            ) : null;
          })}
        </AnimatePresence>
      </Stack>
    </Stack>
  ) : f.status === "error" ? (
    <Stack mt="30vh" mx="auto" width="max-content" alignItems="center" gap={1}>
      <Typography variant="h4">Authentication Failed</Typography>
      <Link component={RouterLink} to="/">
        Go back home.
      </Link>
    </Stack>
  ) : (
    <></>
  );
}

function useLoadingText() {
  const loadingTexts = [
    "Authenticating with secure provider...",
    "Verifying your identity...",
    "Syncing your security credentials...",
    "Confirming sharing privileges...",
    "Checking vault sharing authorization...",
  ];

  const lineCtr = loadingTexts.length;

  const [index, setIndex] = useState(Math.floor(Math.random() * lineCtr));
  useEffect(() => {
    const interval = setInterval(() => {
      const nextIndex = Math.floor(Math.random() * lineCtr);
      setIndex(nextIndex);
    }, 2500);
    return () => clearInterval(interval);
  }, [lineCtr]);

  return { index, loadingTexts };
}

function useAuthGithub() {
  const params = useSearch({ from: "/auth/github" });
  const nav = useNavigate();

  const {
    isPending: loading,
    error,
    status,
  } = useQuery({
    queryKey: ["githubauth"],
    queryFn: () => axios.get("/api/auth/token", { params }),
    retry: 0,
  });

  useEffect(() => {
    if (status === "success") {
      nav({ to: "/dashboard" });
    } else if (status === "error") {
      console.error(error);
    }
  }, [nav, status, error]);

  return { loading, status };
}
