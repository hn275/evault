import {
  createFileRoute,
  Link,
  useLoaderData,
  useSearch,
} from "@tanstack/react-router";
import {
  QueryClient,
  useMutation,
  QueryClientProvider,
} from "@tanstack/react-query";
import { useForm } from "@tanstack/react-form";
import { Button, Stack, TextField } from "@mui/material";
import { Breadcrumbs } from "../../../components/Breadcrumbs";

// Create a client
const queryClient = new QueryClient();

type SearchParams = {
  repo: string;
};

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  component: RouteComponent,
  loader: async ({ params }) => fetchRepoData(parseInt(params.repoID)),
  validateSearch: (search: Record<string, unknown>): SearchParams => {
    const repo = search!.repo as string;
    return { repo };
  },
});

type Status = {
  id: number;
  status: number;
};

async function fetchRepoData(repoID: number): Promise<Status> {
  const r = await fetch(`/api/dashboard/repository/${repoID}`);
  return { id: repoID, status: r.status };
}

function RouteComponent() {
  return (
    <QueryClientProvider client={queryClient}>
      <Page />
    </QueryClientProvider>
  );
}

function Page() {
  const repoID = useLoaderData({ from: "/dashboard/repository/$repoID" });
  const { repo: repoFullName } = useSearch({
    from: "/dashboard/repository/$repoID",
  });

  const breadcrumbs = [
    { display: "Dashboard", href: "/dashboard" },
    { display: repoFullName, href: `https://github.com/${repoFullName}` },
  ];

  return (
    <>
      <Breadcrumbs paths={breadcrumbs} />
      {repoID.status === 440 ? (
        <>
          Session expired. Go back&nbsp;
          <Link to="/">Home.</Link>
        </>
      ) : repoID.status === 200 ? (
        <>Vault found.</>
      ) : repoID.status === 404 ? (
        <>
          <NewVault repoID={repoID.id} repoFullName={repoFullName} />
        </>
      ) : (
        <>Something went wrong.</>
      )}
    </>
  );
}

function NewVault({
  repoID,
  repoFullName,
}: {
  repoID: number;
  repoFullName: string;
}) {
  const { form } = useNewRepository(repoID, repoFullName);
  return (
    <>
      <Stack
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          e.stopPropagation();
          form.handleSubmit();
        }}
      >
        <form.Field
          name="password"
          children={(field) => (
            <>
              <TextField
                label="Password"
                variant="outlined"
                type="password"
                id={field.name}
                name={field.name}
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </>
          )}
        />

        <form.Field
          name="passwordConfirm"
          children={(field) => (
            <>
              <TextField
                label="Re-enter password"
                variant="outlined"
                type="password"
                id={field.name}
                name={field.name}
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </>
          )}
        />

        <form.Subscribe
          selector={(state) => [state.canSubmit, state.isSubmitting]}
          children={([canSubmit, isSubmitting]) => (
            <>
              <Button
                variant="contained"
                type="submit"
                disabled={!canSubmit || isSubmitting}
              >
                {isSubmitting ? "..." : "Submit"}
              </Button>

              {!form.state.isValid && <em>{form.state.errors.join(",")}</em>}
            </>
          )}
        />
      </Stack>
    </>
  );
}

type NewFormProps = {
  password: string;
};

function useNewRepository(repoID: number, repoFullName: string) {
  const mut = useMutation({
    mutationKey: ["newRepoForm"],
    mutationFn: async (formData: NewFormProps) => {
      console.table(formData);
      const params = new URLSearchParams({
        repo_id: `${repoID}`,
        password: formData.password,
        repo_fullname: repoFullName,
      });
      return fetch(`/api/dashboard/repository/new?${params.toString()}`, {
        method: "POST",
      });
    },
  });

  const form = useForm({
    defaultValues: {
      password: "",
      passwordConfirm: "",
    },
    validators: {
      onSubmit: ({ value }) => {
        const { password, passwordConfirm } = value;
        if (password !== passwordConfirm) {
          return "Passwords do not match.";
        }
      },
    },
    onSubmit: async ({ value }) => {
      mut.mutate(value);
    },
  });

  return { form };
}
