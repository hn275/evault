import {
  TextField,
  Button,
  DialogContent,
  DialogActions,
  Stack,
  DialogContentText,
} from "@mui/material";
import { useForm } from "@tanstack/react-form";
import { useMutation } from "@tanstack/react-query";

import DialogTitle from "@mui/material/DialogTitle";
import Dialog from "@mui/material/Dialog";
import { useRouter } from "@tanstack/react-router";
import { useNotifications } from "@toolpad/core/useNotifications";
import { createNewRepository } from "../../../services/repository";

export interface NewVaultDialogProps {
  repoID: number;
  repoFullName: string;
  open: boolean;
  setDialogOpen: (open: boolean) => void;
}

export function NewVault({
  repoID,
  repoFullName,
  open,
  setDialogOpen,
}: NewVaultDialogProps) {
  const { form, cancel } = useNewRepository(
    repoID,
    repoFullName,
    setDialogOpen,
  );
  return (
    <Dialog
      open={open}
      onClose={() => setDialogOpen(false)}
      slotProps={{
        paper: {
          component: "form",
          onSubmit: (e: React.FormEvent<HTMLFormElement>) => {
            e.preventDefault();
            e.stopPropagation();
            form.handleSubmit();
          },
        },
      }}
    >
      <DialogTitle>New Vault</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Create a new vault for this repository.
        </DialogContentText>
        <Stack>
          {/* TODO: This can be refactored into another component */}
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
        </Stack>
      </DialogContent>
      <DialogActions>
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
              <Button variant="outlined" onClick={cancel}>
                Cancel
              </Button>

              {!form.state.isValid && <em>{form.state.errors.join(",")}</em>}
            </>
          )}
        />
      </DialogActions>
    </Dialog>
  );
}

type NewFormProps = {
  password: string;
};

function useNewRepository(
  repoID: number,
  repoFullName: string,
  setDialogOpen: (open: boolean) => void,
) {
  const router = useRouter();
  const notifications = useNotifications();
  const mut = useMutation({
    mutationKey: ["newRepoForm"],
    mutationFn: async (formData: NewFormProps) => {
      // TODO: Refactor this into a service file
      // TODO: Add loading indicator
      console.table(formData);
      const params = new URLSearchParams({
        repo_id: `${repoID}`,
        password: formData.password,
        repo_fullname: repoFullName,
      });
      return createNewRepository(params)
        .then((r) => {
          if (r.status === 201 || r.status === 200) {
            setDialogOpen(false);
            router.invalidate();
            notifications.show("Vault created successfully", {
              severity: "success",
              autoHideDuration: 3000,
            });
          }
          return r;
        })
        .catch((e) => {
          notifications.show("Failed to create vault", {
            severity: "error",
            autoHideDuration: 3000,
          });
          throw e;
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

  const cancel = () => {
    form.reset();
    setDialogOpen(false);
    router.history.back();
  };

  return { form, cancel };
}
