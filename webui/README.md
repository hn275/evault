# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ["./tsconfig.node.json", "./tsconfig.app.json"],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    "react-x": reactX,
    "react-dom": reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs["recommended-typescript"].rules,
    ...reactDom.configs.recommended.rules,
  },
});
```

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
