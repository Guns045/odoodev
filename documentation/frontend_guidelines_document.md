# Frontend Guideline Document for odoodev

This document outlines the frontend setup and best practices for the `odoodev` project. It is meant to guide developers, designers, and contributors without assuming deep technical expertise. By following these guidelines, the team can build a consistent, scalable, and user-friendly interface to host and present Odoo tutorials.

## 1. Frontend Architecture

### Overview
- We use **React** as our main framework to build a Single Page Application (SPA). React lets us break the interface into small, reusable pieces called components.
- For project setup and quick builds, we choose **Vite**. It offers fast startup times and simple configuration.
- We keep the folder structure clear and predictable, so new team members can find code quickly.

### Scalability, Maintainability, Performance
- **Component-based structure** ensures that each part of the UI lives in its own folder. This makes it easy to add, remove, or update features independently.
- **Lazy loading** and **code splitting** (loading only the code needed for each page) keep initial load times low, improving performance.
- **Clear naming and folder conventions** reduce confusion as the codebase grows.

## 2. Design Principles

We guide our work with three main values:

1. **Usability**  
   - Interfaces should be intuitive. Buttons, links, and forms behave as users expect.  
   - We use clear labels and provide helpful messages when something goes wrong.

2. **Accessibility**  
   - We follow basic accessibility rules (such as proper heading order and keyboard navigation) so everyone, including people with disabilities, can use the site.  
   - We add simple ARIA attributes where needed and test with screen readers.

3. **Responsiveness**  
   - Our UI adjusts gracefully to different screen sizes, from mobile phones to large desktop monitors.  
   - We use relative units (like `em` and `rem`) and flexible layouts (using CSS Grid or Flexbox).

## 3. Styling and Theming

### Styling Approach
- We use **Tailwind CSS**, a utility-first framework. It lets us apply small, descriptive classes directly in our markup (for example, `mt-4`, `text-center`).
- Tailwind configuration lives in `tailwind.config.js`, where we can customize colors, fonts, and spacing.

### Theming
- All colors and font sizes are defined in our Tailwind theme. This keeps the look and feel consistent across all pages and components.
- We support a **light** and **dark** mode by toggling a single CSS class on the `<html>` element.

### Visual Style
- Style: **Modern Flat**. Clean lines, simple shapes, and minimal visual noise.  
- Color palette:  
  • Primary Blue: `#1E40AF`  
  • Secondary Green: `#10B981`  
  • Background Light: `#F9FAFB`  
  • Background Dark: `#111827`  
  • Text Dark: `#111827`  
  • Text Light: `#FFFFFF`  
- Font: **Inter**, a modern sans-serif font with good readability on screens. We import it via Google Fonts in `index.html`.

## 4. Component Structure

We organize components by their role and reusability:

- `/src/components/atoms/`  
  • Small, standalone elements (e.g., Buttons, Icons, Inputs)
- `/src/components/molecules/`  
  • Combinations of atoms (e.g., FormGroup, CardHeader)
- `/src/components/organisms/`  
  • Larger sections that form distinct parts of a page (e.g., Navbar, TutorialList)
- `/src/components/templates/`  
  • Full page layouts (e.g., MainLayout, AuthLayout)

This approach:
- Makes it easy to find and reuse code.
- Lets us swap or update parts without affecting other areas.

## 5. State Management

### Approach
- We use **React Context + useReducer** for global state. This simple pattern covers most needs without adding heavy dependencies.
- For complex scenarios (like caching tutorial data), we rely on **React Query**, which handles data fetching and caching automatically.

### Sharing State
- A `TutorialProvider` wraps the app and provides the list of tutorials and user preferences (like dark mode).
- Components can read or update state by using the `useContext` hook.

## 6. Routing and Navigation

- We use **React Router v6** to handle page navigation in our SPA.
- Routes are defined in `/src/App.jsx`:  
  • `/` – Home page with an introduction and tutorial catalog.  
  • `/tutorial/:id` – Tutorial detail page.  
  • `/about` – About the project.  
- Navigation happens without full page reloads, creating a smooth experience.

## 7. Performance Optimization

Key strategies:

- **Code splitting**: Use React’s `lazy()` and `Suspense` to load pages or heavy components only when needed.
- **Image optimization**: Serve appropriately sized images using modern formats like WebP.
- **Production build tweaks**: Enable minification, tree-shaking, and gzip compression via Vite.
- **Caching**: Use service workers or HTTP cache headers to keep frequently used assets on the client side.

These measures help pages load quickly and stay responsive.

## 8. Testing and Quality Assurance

### Unit Testing
- **Jest** with **React Testing Library** for testing individual components. We focus on what the user sees and interacts with.

### Integration Testing
- Combine related components to ensure they work together. We also mock API calls using **Mock Service Worker (msw)**.

### End-to-End Testing
- **Cypress** runs through real user flows (like opening a tutorial, marking lessons as complete) to catch issues early.

### Linting and Formatting
- **ESLint** enforces code style and catches errors.  
- **Prettier** auto-formats code.  
- We use pre-commit hooks (via **Husky**) to run these tools before every commit.

## 9. Conclusion and Overall Frontend Summary

By following these guidelines, the `odoodev` frontend will remain:

- **Scalable**: Clear architecture and folder structure support growth.  
- **Maintainable**: Consistent code patterns and shared components reduce duplication.  
- **Performant**: Optimizations ensure fast loading and smooth interactions.  
- **User-friendly**: Design principles of usability, accessibility, and responsiveness keep learners engaged.

This setup is tailored to host Odoo tutorials in a clean, modern interface, fostering an enjoyable learning experience for everyone.