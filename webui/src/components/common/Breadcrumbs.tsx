import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Fragment } from "react/jsx-runtime";

type PathProps = {
  display: string;
  href: string;
};

type BreadcrumbsProps = {
  paths: PathProps[];
};

export function Breadcrumbs({ paths }: BreadcrumbsProps) {
  return (
    <Breadcrumb>
      <BreadcrumbList>
        {paths.map((path) => (
          <Fragment key={path.href}>
            <BreadcrumbItem>
              <BreadcrumbLink
                href={path.href}
                target={path.href.startsWith("http") ? "_blank" : "_self"}
              >
                {path.display}
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
          </Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  );
}
