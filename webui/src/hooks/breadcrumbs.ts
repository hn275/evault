import { useEffect } from "react";
import { setBreadcrumbs } from "@/store/breadcrumbsStore";
import type { Breadcrumbs } from "@/types/Breadcrumb";

/**
 * Custom hook to set breadcrumbs with automatic cleanup
 * @param breadcrumbs - The breadcrumb configuration to set
 * @param deps - Dependencies array for the useEffect
 */
export function useBreadcrumbs(
  breadcrumbs: Breadcrumbs,
  deps: React.DependencyList = [],
) {
  useEffect(() => {
    setBreadcrumbs(breadcrumbs);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}

/**
 * Convenience hook for setting simple breadcrumbs with paths
 * @param paths - Array of path objects
 * @param deps - Dependencies array for the useEffect
 */
export function useBreadcrumbPaths(
  paths: Breadcrumbs["paths"],
  deps: React.DependencyList = [],
) {
  useBreadcrumbs({ paths }, deps);
}
