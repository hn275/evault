import { Breadcrumbs as MUIBreadcrumbs, Link } from "@mui/material";

type PathProps = {
  display: string;
  href: string;
};

type BreadcrumbsProps = {
  paths: PathProps[];
};

export function Breadcrumbs({ paths }: BreadcrumbsProps) {
  return (
    <div role="presentation">
      <MUIBreadcrumbs aria-label="breadcrumb">
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
    </div>
  );
}
