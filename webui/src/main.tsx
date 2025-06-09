import { createBrowserRouter, RouterProvider } from "react-router";
import { createRoot } from "react-dom/client";
import Home from "./App";
import { Auth, AuthGithub } from "./pages/auth";
import { Dash } from "./pages/dash";

let router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
    children: [],
  },
  { path: "/auth", Component: Auth },
  { path: "/auth/github", Component: AuthGithub },
  { path: "/dashboard", Component: Dash },
]);

createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />,
);
