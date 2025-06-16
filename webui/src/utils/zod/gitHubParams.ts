import { z } from "zod/v4";

export const paramParser = z.object({
  session_id: z.string(),
  device_type: z.enum(["web", "cli"]),
  code: z.string(),
  state: z.string(),
});

export type GitHubOAuthSearchParams = z.infer<typeof paramParser>;

export type GitHubOAuthSearchParamResult =
  z.ZodSafeParseResult<GitHubOAuthSearchParams>;
