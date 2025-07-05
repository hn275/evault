import { Spinner } from "../ui/spinner";

// This is a component that displays a loader with a text
export function LoaderWithText({ text }: { text: string }) {
  return (
    <div className="flex flex-col justify-center items-center min-h-40">
      <Spinner size="large" />
      <p className="text-2xl text-muted-foreground">{text}</p>
    </div>
  );
}
