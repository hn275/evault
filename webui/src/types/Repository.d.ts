import {
  repoOwnerSchema,
  repoSchema,
  reposSchema,
} from "@/lib/validator/repository";
import { z } from "zod/v4";

export type Repository = z.infer<typeof repoSchema>;
export type Repositories = z.infer<typeof reposSchema>;
export type RepoOwner = z.infer<typeof repoOwnerSchema>;
