# Skill: Implementation — Frontend

Purpose: implement user-facing frontend components, pages, and interactions with accessibility and responsive design in mind.

When to use:
- Building web UI, dashboards, forms, and client-side data handling for `djassa`.

Recommended stack guidance (suggested):
- Framework: `React` with TypeScript or `Vue 3` with Composition API.
- Styling: utility CSS (`Tailwind`) or component library (`Chakra UI` / `MUI`).
- State: local component state for simple screens; `React Query` or `SWR` for server state; `zustand` or `Redux` for complex global state.
- Testing: component tests with `@testing-library/react`, end-to-end with `Playwright` or `Cypress`.

Key deliverables:
- Small component library and storybook-like examples (or docs) for shared components.
- Accessible forms and validation with clear error states.
- Integration examples showing API calls to backend endpoints with mock server or MSW.

Prompt patterns:
- Task: "Create a `PaymentForm` component that posts payment data to `/api/payments`, shows success and error states, and includes unit and e2e tests."

Contributor notes:
- Include design tokens and breakpoints in a central file. Write clear props documentation.
