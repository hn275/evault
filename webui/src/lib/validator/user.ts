import { z } from "zod/v4";

export const userSchema = z.strictObject({
  id: z.number(),
  login: z.string(),
  avatar_url: z.string(),
  name: z.string(),
  type: z.string(),
});
