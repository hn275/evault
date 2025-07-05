import { QueryClientProvider } from "@tanstack/react-query";
import { createRootRoute, HeadContent, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { queryClient } from "../utils/queryClient";
import { Toaster } from "@/components/ui/sonner";

export const Route = createRootRoute({
  component: () => (
    <QueryClientProvider client={queryClient}>
      <HeadContent />

        <Toaster position="top-right" duration={3000} richColors />
        <Outlet />
        <TanStackRouterDevtools />
    </QueryClientProvider>
  ),
});
