import { QueryClientProvider } from "@tanstack/react-query";
import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { NotificationsProvider } from "@toolpad/core/useNotifications";
import { queryClient } from "../utils/queryClient";

export const Route = createRootRoute({
  component: () => (
    <QueryClientProvider client={queryClient}>
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
