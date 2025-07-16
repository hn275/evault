import { z } from "zod/v4";

export const repoOwnerSchema = z.strictObject({
  id: z.number(),
  login: z.string(),
  avatar_url: z.string(),
});

export const repoSchema = z.strictObject({
  id: z.number(),
  full_name: z.string(),
  private: z.boolean(),
  html_url: z.string(),
  description: z.string().nullable(),
  owner: repoOwnerSchema,
});

export const reposSchema = z.array(repoSchema);
