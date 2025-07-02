import { Container } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";
import { Outlet } from "@tanstack/react-router";
import DashboardNavbar from "../components/dashboard/Navbar";

export const Route = createFileRoute("/dashboard")({
  component: LayoutComponent,
});

function LayoutComponent() {
  // TODO: user needs to be logged in to access the dashboard if user is not logged in, redirect to the login page

  return (
    <>
      <DashboardNavbar />
      <Container maxWidth="xl">
        <Outlet />
      </Container>
    </>
  );
}
