import { QueryClientProvider } from "@tanstack/react-query";
import { createRootRoute, HeadContent, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { NotificationsProvider } from "@toolpad/core/useNotifications";
import { queryClient } from "../utils/queryClient";

export const Route = createRootRoute({
  component: () => (
    <QueryClientProvider client={queryClient}>
      <HeadContent />

      <NotificationsProvider
        slotProps={{
          snackbar: {
            anchorOrigin: { vertical: "top", horizontal: "right" },
          },
        }}
      >
        <Outlet />
        <TanStackRouterDevtools />
      </NotificationsProvider>
    </QueryClientProvider>
  ),
});
