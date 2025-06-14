import { Stack, TextField, Button } from "@mui/material";
import { useForm } from "@tanstack/react-form";
import { useMutation } from "@tanstack/react-query";

export function NewVault({
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
