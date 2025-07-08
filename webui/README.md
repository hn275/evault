# eVault UI

## ShadCN UI library

### Overview

This project uses **ShadCN UI** as the primary component library, providing a comprehensive set of accessible, customizable, and modern UI components built on top of Radix UI primitives and styled with Tailwind CSS.

We're using tweakcn's Caffeine theme for our UI theme, example can be found here https://tweakcn.com/.

#### Color Palette

- **Background/Foreground**: Main surface colors
- **Primary**: Main brand color for actions
- **Secondary**: Secondary actions and elements
- **Muted**: Subtle text and backgrounds
- **Accent**: Hover states and highlights
- **Destructive**: Error and danger states
- **Border/Input**: Form and border colors

### Usage Patterns

#### Basic Import and Usage

```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

// Basic usage
<Button variant="default" size="sm">
  Click me
</Button>;
```

#### Component Composition

Complex components are built by composing multiple ShadCN primitives:

```tsx
// Example from NewVaultForm.tsx
<Dialog open={open} onOpenChange={setDialogOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>New Vault</DialogTitle>
      <DialogDescription>
        Please enter a password to create a new vault.
      </DialogDescription>
    </DialogHeader>

    <Input
      type="password"
      className="my-1"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
    />

    <DialogFooter>
      <Button variant="default" type="submit">
        Submit
      </Button>
      <Button variant="outline" onClick={cancel}>
        Cancel
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

#### Styling with Class Variants

Components use `class-variance-authority` (CVA) for variant management:

```tsx
// Button variants
<Button variant="default">Primary Action</Button>
<Button variant="outline">Secondary Action</Button>
<Button variant="destructive">Delete</Button>
<Button variant="ghost">Subtle Action</Button>

// Size variants
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
```

#### Custom Styling

Use the `cn()` utility function for conditional classes:

```tsx
import { cn } from "@/lib/utils";

<Button
  className={cn(
    "custom-class",
    isLoading && "opacity-50",
    variant === "special" && "bg-gradient-to-r from-blue-500 to-purple-600",
  )}
>
  Custom Button
</Button>;
```

### Architecture Integration

#### Component Organization

```md
src/
├── components/
│ ├── ui/ # ShadCN UI components
│ ├── common/ # Shared app components
│ └── dashboard/ # Feature-specific components
├── lib/
│ └── utils.ts # Utility functions (cn, etc.)
└── routes/ # Route components
```

#### Import Patterns

```tsx
// UI components (ShadCN)
import { Button } from "@/components/ui/button";

// Application components
import { RepositoryCard } from "@/components/dashboard/RepositoryCard";

// Common utilities
import { cn } from "@/lib/utils";
```

### Best Practices

#### 1. Component Composition

- Use compound components (Dialog, DialogContent, DialogHeader, etc.)
- Prefer composition over complex prop APIs
- Keep components focused on single responsibilities

#### 2. Styling Guidelines

- Use CSS variables for consistent theming
- Leverage component variants instead of custom CSS
- Use `cn()` for conditional styling
- Maintain consistent spacing using Tailwind classes

#### 3. Accessibility

- ShadCN components come with built-in accessibility features
- Always provide proper labels and descriptions
- Use semantic HTML elements through component props

#### 4. Performance

- Import only needed components
- Use `asChild` prop for polymorphic components when needed
- Leverage React.memo for expensive re-renders if necessary

### Example Usage in Codebase

#### Navigation with Breadcrumbs

```tsx
// From Breadcrumbs.tsx
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/repository">Repository</BreadcrumbLink>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>;
```

#### User Profile Display

```tsx
// From dashboard/index.tsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

<Avatar>
  <AvatarImage src={user.avatar_url} alt={user.name} />
  <AvatarFallback>{user.name[0]}</AvatarFallback>
</Avatar>;
```

#### Loading States

```tsx
// Loading skeleton
import { Skeleton } from "@/components/ui/skeleton";

<div className="space-y-2">
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-3/4" />
  <Skeleton className="h-4 w-1/2" />
</div>;

// Loading spinner
import { Spinner } from "@/components/ui/spinner";

<Spinner size="medium" show={isLoading}>
  Loading...
</Spinner>;
```

### Customization and Extension

#### Adding New Components

To add a new ShadCN component:

1. Use the ShadCN CLI: `npx shadcn-ui@latest add [component-name]`
2. Components will be automatically added to `src/components/ui/`
3. Import and use throughout the application

#### Theme Customization

Modify CSS variables in `src/index.css` to customize the theme:

```css
:root {
  --radius: 0.5rem; /* Adjust border radius */
  --primary: oklch(0.3 0.2 250); /* Change primary color */
}
```

#### Custom Variants

Extend component variants by modifying the CVA configuration:

```tsx
// In a component file
const buttonVariants = cva(
  "...", // base classes
  {
    variants: {
      variant: {
        // ... existing variants
        custom: "bg-gradient-to-r from-pink-500 to-violet-500",
      },
    },
  },
);
```

### Troubleshooting

#### Common Issues

1. **Import Errors**: Ensure path aliases are correctly configured in `tsconfig.json`
2. **Styling Issues**: Check if CSS variables are properly loaded
3. **Theme Not Applied**: Verify dark mode class toggling works correctly

#### Development Tips

- Use browser dev tools to inspect CSS variable values
- Test components in both light and dark modes
- Verify accessibility with screen readers
- Check responsive behavior across different screen sizes

## Architecture

The following are guidelines for what goes where within the code base, please note these are guidelines and not strict rules since React can have limitations.

### Directory Structure Guidelines

- `/src/routes/` - Contains all route components and their associated logic

- `/src/components/` - Reusable UI components
  - `/dashboard/` - Dashboard-specific components
  - `/common/` - Shared components used across multiple features

- `/src/services/` - API and service layer
  - `common.ts` - Shared service utilities

- `/src/hooks/` - Custom React hooks

- `/src/utils/` - Utility functions and helpers
  - `/zod/` - Zod schema definitions and parsers

- `/src/types/` - TypeScript type definitions

### File Organization Principles

1. **Route Components**
   - Keep route components simple and focused on routing logic
   - Try to put all business logics to hooks
   - Delegate complex UI to separate components
   - Queries should be declared here, unless we really need it in the route components

2. **Components**
   - Route-specific components go in the corresponding folder path
   - Keep components small and focused on a single responsibility
   - On mutations should be declared on the route-specific components, queries should be very rarely needed to be declared here

3. **Services**
   - One service file per data type (ie. repository, auth)
   - Keep API calls and data transformation logic here
   - Use common utilities for shared functionality (ie. if we need to add a redirect to all authenticated API calls)

4. **Hooks**
   - Extract reusable logic into custom hooks
   - Group related hooks by feature
   - Keep hooks focused on a single concern
   - If libraries like Tanstack Query already has majority of the hook's functionality covered, a hook should not be created

5. **Types**
   - For Props, define where the component is
   - For shared types across files, define within the folder

### Guidelines for new routes

- Any new routes **MUST** have a declared title under head property of the route declaration.
