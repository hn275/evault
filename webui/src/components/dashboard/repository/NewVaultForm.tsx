import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog";
import { useForm } from "@tanstack/react-form";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "@tanstack/react-router";
import { createNewRepository } from "../../../services/repository";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

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
    <>
      <Dialog
        open={open}
        onOpenChange={(open) => {
          setDialogOpen(open);
          if (!open) {
            cancel();
          }
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>New Vault</DialogTitle>
            <DialogDescription>
              Please enter a password to create a new vault for this repository.
            </DialogDescription>
          </DialogHeader>
          <div className="flex flex-col gap-2">
            {/* TODO: This can be refactored into another component */}
            <form.Field
              name="password"
              children={(field) => (
                <Input
                  type="password"
                  size={1}
                  className="my-1"
                  id={field.name}
                  name={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                />
              )}
            />

            <form.Field
              name="passwordConfirm"
              children={(field) => (
                <Input
                  type="password"
                  size={1}
                  className="my-1"
                  id={field.name}
                  name={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                />
              )}
            />
          </div>

          <DialogFooter>
            <form.Subscribe
              selector={(state) => [state.canSubmit, state.isSubmitting]}
              children={([canSubmit, isSubmitting]) => (
                <>
                  <Button
                    variant="default"
                    type="submit"
                    disabled={!canSubmit || isSubmitting}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      form.handleSubmit();
                    }}
                  >
                    {isSubmitting ? "..." : "Submit"}
                  </Button>
                  <DialogClose asChild>
                    <Button variant="outline" onClick={cancel}>
                      Cancel
                    </Button>
                  </DialogClose>

                  {!form.state.isValid && (
                    <em>{form.state.errors.join(",")}</em>
                  )}
                </>
              )}
            />
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

type NewFormProps = {
  password: string;
};

// TODO: I don't think this hook is doing anything extra that needs to be handled through a hook, honestly putting this all in the component will be easier to understand and maintain.
function useNewRepository(
  repoID: number,
  repoFullName: string,
  setDialogOpen: (open: boolean) => void,
) {
  const router = useRouter();
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
            toast.success("Vault created successfully");
          }
          return r;
        })
        .catch((e) => {
          toast.error("Failed to create vault");
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
