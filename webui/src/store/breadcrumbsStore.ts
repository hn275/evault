import type { Breadcrumbs } from "@/types/Breadcrumb";
import { create } from "zustand";

interface BreadcrumbsState {
  breadcrumbs: Breadcrumbs;
}

const useBreadcrumbsStore = create<BreadcrumbsState>()((set) => ({
  breadcrumbs: { paths: [] },
  setBreadcrumbs: (breadcrumbs: Breadcrumbs) => set({ breadcrumbs }),
}));

// best practices for zustand stores is to use a hook to access the store
export const useBreadcrumbs = () => {
  return useBreadcrumbsStore((state) => state.breadcrumbs);
};

// Separate function for business logic
export const setBreadcrumbs = (breadcrumbs: Breadcrumbs) => {
  useBreadcrumbsStore.setState({ breadcrumbs });
};
