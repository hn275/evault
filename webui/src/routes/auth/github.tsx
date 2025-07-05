import { createFileRoute, Link, Navigate } from "@tanstack/react-router";
import {
  paramParser,
  type GitHubOAuthSearchParamResult,
} from "../../utils/zod/gitHubParams";
import { useAuthGithub } from "../../hooks/auth";
import { AnimatePresence, motion } from "motion/react";
import { useLoadingText } from "../../hooks/loadingText";
import { Spinner } from "@/components/ui/spinner";

const TEXT_CHANGE_INTERVAL = 3000; // milliseconds
const loadingTexts = [
  "Authenticating with secure provider...",
  "Verifying your identity...",
  "Syncing your security credentials...",
  "Confirming sharing privileges...",
  "Checking vault sharing authorization...",
];

export const Route = createFileRoute("/auth/github")({
  head: () => ({
    meta: [
      {
        title: "Authenticating with GitHub | Evault",
      },
    ],
  }),
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
    <div className="pt-[30vh] mx-auto w-max flex flex-col items-center gap-1 h-screen">
      <h4 className="text-2xl">Authentication Failed</h4>
      <Link to="/">
        Go back home.
      </Link>
    </div>
  );
}

function LoadingState() {
  const { index } = useLoadingText(TEXT_CHANGE_INTERVAL, loadingTexts);

  return (
    <div className="pt-[30vh] mx-auto w-max flex flex-col items-center gap-4 h-screen">
      <h4 className="text-2xl">
        Authenticating with GitHub
      </h4>

      <div className="flex flex-col items-center gap-2">
        <Spinner size="large" />
        <AnimatePresence mode="wait">
          {loadingTexts.map((text, idx) => {
            return index === idx ? (
              <motion.div
                key={`text-key-${idx}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
              >
                <p className="text-sm text-muted-foreground">
                  {text}
                </p>
              </motion.div>
            ) : null;
          })}
        </AnimatePresence>
      </div>
    </div>
  );
}
