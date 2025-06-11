import { createFileRoute, useLoaderData } from "@tanstack/react-router";
import {
  QueryClient,
  useMutation,
  QueryClientProvider,
} from "@tanstack/react-query";
import { useForm, type AnyFieldApi } from "@tanstack/react-form";
import { Button, TextField } from "@mui/material";
import { useEffect } from "react";

// Create a client
const queryClient = new QueryClient();

export const Route = createFileRoute("/dashboard/repository/$repoID")({
  component: RouteComponent,
  loader: async ({ params }) => fetchRepoData(parseInt(params.repoID)),
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
  const repo = useLoaderData({ from: "/dashboard/repository/$repoID" });

  const { form } = useNewRepository();

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          e.stopPropagation();
          form.handleSubmit();
        }}
      >
        <form.Field
          name="repo_id"
          children={() => (
            <>
              <input name="repo_id" type="hidden" value={repo.id} />
            </>
          )}
        />

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
              <FieldInfo field={field} />
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

              <FieldInfo field={field} />
            </>
          )}
        />

        <form.Subscribe
          selector={(state) => [state.canSubmit, state.isSubmitting]}
          children={([canSubmit, isSubmitting]) => (
            <Button
              variant="contained"
              type="submit"
              disabled={form.state.isSubmitting}
            >
              {isSubmitting ? "..." : "Submit"}
            </Button>
          )}
        />
      </form>
    </>
  );
}

function FieldInfo({ field }: { field: AnyFieldApi }) {
  useEffect(() => console.log(field), [field]);
  // console.log(field.state.meta);
  return (
    <>
      {field.state.meta.isTouched && !field.state.meta.isValid ? (
        <em>{field.state.meta.errors.join(", ")}</em>
      ) : null}
      {field.state.meta.isValidating ? "Validating..." : null}
      {field.state.meta.errors.length !== 0 ? (
        field.state.meta.errorMap.onSubmit
      ) : (
        <></>
      )}
    </>
  );
}

type NewFormProps = {
  repo_id: number;
  password: string;
  passwordConfirm: string;
};

function useNewRepository() {
  const mut = useMutation({
    mutationKey: ["newRepoForm"],
    mutationFn: async (data: NewFormProps) => {
      return new Promise((resolve) => {
        setTimeout(() => {
          console.log(data);
          resolve(data);
        }, 1000);
      }).then((_) => {});
    },
  });

  const form = useForm({
    defaultValues: {
      password: "",
      passwordConfirm: "",
      repo_id: "",
    },
    validators: {
      onSubmit: ({ value }) => {
        const { password, passwordConfirm } = value;
        if (password !== passwordConfirm) {
          const errMsg = "Passwords do not match.";
          return {
            password: errMsg,
            passwordConfirm: errMsg,
          };
        }

        return null;
      },
    },
    onSubmit: async ({ value }) => {
      mut.mutate({
        repo_id: parseInt(value.repo_id),
        password: value.password,
        passwordConfirm: value.passwordConfirm,
      });
    },
  });

  return { form };
}
