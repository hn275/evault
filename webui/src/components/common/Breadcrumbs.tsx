import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { useBreadcrumbs } from "@/store/breadcrumbsStore";
import type { Breadcrumbs } from "@/types/Breadcrumb";
import { Link } from "@tanstack/react-router";
import { Fragment } from "react/jsx-runtime";

export function Breadcrumbs() {
  const breadcrumbs = useBreadcrumbs();
  return (
    <Breadcrumb>
      <BreadcrumbList>
        {breadcrumbs.paths.map((path) => (
          <Fragment key={path.href}>
            <BreadcrumbItem>
              <Link
                className="hover:bg-black/10 dark:hover:bg-white/10 rounded-md p-1"
                to={path.href}
                target={path.href.startsWith("http") ? "_blank" : "_self"}
              >
                {path.display}
              </Link>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
          </Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  );
}
