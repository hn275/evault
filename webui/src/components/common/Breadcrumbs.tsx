import { Breadcrumbs as MUIBreadcrumbs, Link, type Theme, type SxProps } from "@mui/material";

type PathProps = {
  display: string;
  href: string;
};

type BreadcrumbsProps = {
  paths: PathProps[];
  sx?: SxProps<Theme>;
};

export function Breadcrumbs({ paths, ...props }: BreadcrumbsProps) {
  return (
      <MUIBreadcrumbs aria-label="breadcrumb" {...props}>
        {paths.map((path) => (
          <Link
            underline="hover"
            color="inherit"
            href={path.href}
            target={path.href.startsWith("http") ? "_blank" : "_self"}
          >
            {path.display}
          </Link>
        ))}
      </MUIBreadcrumbs>
  );
}
