# Knowledge Base 02: Interactive Frontend & Workspace

This document captures the distilled learnings and technical hurdles identified during the development of the **Interactive Workspace** UI.

## Hurdle: Vue 3 Event Argument Handling
- **Problem**: Attempting to use `$arguments` in a Vue 3 template to access emitted data caused a "Property '$arguments' does not exist" error.
- **Learning**: Nuxt 4 (Vue 3) does not provide a global `$arguments` variable.
- **Solution**: Refactored children to emit data directly: `emit('drag-start', event, payload)`. The parent then uses a standard method handler: `@drag-start="handleDrag"`.

## Decision: Glassmorphism Implementation
- **Why**: Standard opaque backgrounds felt "heavy" and non-premium.
- **Learning**: `backdrop-blur` and `bg-opacity` in Tailwind are enough for the effect, but border contrast is essential for depth.
- **Implementation**: Used `bg-gray-900/50 backdrop-blur-md border border-white/10`.

## Hurdle: Icon Scaling & Nuxt UI
- **Context**: Icons in the Table Registry appeared distorted or truncated in some viewports.
- **Learning**: Standard SVG scaling in Nuxt UI can be overridden by parent flex/grid constraints if `flex-shrink` is not managed.
- **Solution**: Applied `flex-shrink-0` to all icon containers and ensured uniform scaling via localized CSS variables.

---

## Technical Definitions

| Term | Definition |
|------|------------|
| **Glassmorphism** | A design trend characterized by glass-like transparency, background blur, and subtle highlights. |
| **Pinia** | The intuitive, type-safe store for Vue 3 that facilitates state management across components. |
| **Debouncing** | A programming practice used to ensure that time-consuming tasks do not fire so often that they make the web page unresponsive. |

> [!NOTE]
> **Client-Side Rendering (CSR)**: We use `<ClientOnly>` wrappers for the ER Diagram and Drag-and-Drop zones to avoid hydration mismatches, as these components rely on browser-only APIs like `window` and `document`.
