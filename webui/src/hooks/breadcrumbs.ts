import { useEffect } from "react";
import { setBreadcrumbs } from "@/store/breadcrumbsStore";
import type { Breadcrumbs } from "@/types/Breadcrumb";

// Custom hook to set breadcrumbs with automatic cleanup
export function useBreadcrumbs(
  breadcrumbs: Breadcrumbs,
  deps: React.DependencyList = [],
) {
  useEffect(() => {
    setBreadcrumbs(breadcrumbs);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}

// Setting the path using the code we've been using
export function useBreadcrumbPaths(
  paths: Breadcrumbs["paths"],
  deps: React.DependencyList = [],
) {
  useBreadcrumbs({ paths }, deps);
}
