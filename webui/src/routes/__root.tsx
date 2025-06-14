import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { NotificationsProvider } from "@toolpad/core/useNotifications";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export const Route = createRootRoute({
  component: () => (
    <NotificationsProvider
      slotProps={{
        snackbar: {
          anchorOrigin: { vertical: "top", horizontal: "right" },
        },
      }}
    >
      <QueryClientProvider client={queryClient}>
        <div className="p-2 flex gap-2">
          <Link to="/" className="[&.active]:font-bold">
            Home
          </Link>{" "}
        </div>
        <hr />
        <Outlet />
        <TanStackRouterDevtools />
      </QueryClientProvider>
    </NotificationsProvider>
  ),
});
