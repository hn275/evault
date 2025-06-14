import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { Outlet } from "@tanstack/react-router";

export const Route = createFileRoute("/dashboard")({
  component: LayoutComponent,
});

function LayoutComponent() {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  );
}
