import { QueryClientProvider } from "@tanstack/react-query";
import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
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
        <div className="p-2 flex gap-2">
          <Link to="/" className="[&.active]:font-bold">
            Home
          </Link>{" "}
        </div>
        <hr />
        <Outlet />
        <TanStackRouterDevtools />
      </NotificationsProvider>
    </QueryClientProvider>
  ),
});
