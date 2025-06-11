import { createFileRoute, useLoaderData } from "@tanstack/react-router";
import { useEffect } from "react";
import {
  QueryClient,
  useMutation,
  QueryClientProvider,
} from "@tanstack/react-query";
import { useForm } from "@tanstack/react-form";

// Create a client
const queryClient = new QueryClient();

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  component: RouteComponent,
  loader: async ({ params }) => fetchRepoData(parseInt(params.repoID)),
});

type Repository = {
  id: number;
};

type ServerError = number; // http status code

async function fetchRepoData(
  repoID: number,
): Promise<Repository | ServerError | null> {
  const r = await fetch(`/api/dashboard/repository/${repoID}`);
  switch (r.status) {
    case 200:
      return { id: repoID };
    case 404:
      return null;
    default:
      return r.status;
  }
}

function RouteComponent() {
  const repo = useLoaderData({ from: "/dashboard/repository/$repoID" });
  useEffect(() => console.log(repo), [repo]);

  const { form } = useNewRepository();

  return (
    <QueryClientProvider client={queryClient}>
      {repo === null ? (
        <>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              e.stopPropagation();
              form.handleSubmit();
            }}
          >
            <form.Field
              name="password"
              children={(field) => (
                <input
                  type="password"
                  id={field.name}
                  name={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                />
              )}
            />
            <form.Subscribe
              selector={(state) => [state.canSubmit, state.isSubmitting]}
              children={([canSubmit, isSubmitting]) => (
                <button type="submit" disabled={!canSubmit}>
                  {isSubmitting ? "..." : "Submit"}
                </button>
              )}
            />
          </form>
        </>
      ) : typeof repo === "number" ? (
        <>{repo}</>
      ) : (
        <>
          <section>Hello {` /dashboard/repository/${repo!.id}`}!</section>
        </>
      )}
    </QueryClientProvider>
  );
}

type NewFormProps = {
  repo_id: string;
  password: string;
};

function useNewRepository() {
  const mut = useMutation({
    mutationKey: ["newRepoForm"],
    mutationFn: async (data: NewFormProps) => {
      return new Promise((resolve) => resolve("ok")).then((_) => {
        console.log(data);
      });
    },
  });

  const form = useForm({
    defaultValues: {
      password: "",
    },
    onSubmit: async ({ value }) => {
      mut.mutate({
        repo_id: "123",
        password: value.password,
      });
      console.log(value);
    },
  });

  return { form };
}
