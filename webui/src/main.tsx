import { createBrowserRouter, RouterProvider } from "react-router";
import { createRoot } from "react-dom/client";
import Home from "./App";
import { Auth } from "./pages/auth";

let router = createBrowserRouter([
	{
		path: "/",
		Component: Home,
		children: [
			/*
						{
							path: "shows/:showId",
							Component: Show,
							loader: ({ request, params }) =>
								fetch(`/api/show/${params.showId}.json`, {
									signal: request.signal,
								}),
						},
						*/
		],
	},
	{
		path: "/auth",
		Component: Auth,
	},
]);

createRoot(document.getElementById("root")).render(
	<RouterProvider router={router} />,
);
