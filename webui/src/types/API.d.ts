import { userValidator } from "@/lib/validator/user";
import { z } from "zod/v4";

export type User = z.infer<typeof userValidator>;

export type Status = {
  id: number;
  status: number;
};
