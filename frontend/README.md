# Entity Canvas: Frontend

This is the **Nuxt 4** powered frontend for Entity Canvas. It provides a visual, interactive workspace for schema discovery and SQL construction.

## 🚀 Built With
- **Framework**: Nuxt 4 (Vue 3)
- **UI & Icons**: Nuxt UI (Tailwind CSS)
- **State Management**: Pinia
- **Interactivity**: vuedraggable, standard Vue event-bus patterns

## 📂 Structure
- `app/components/QueryBuilder/`: Core visual building blocks (Select/Filter zones).
- `app/components/Workspace/`: High-level layout components (ER Canvas, Panes).
- `app/pages/`: Nuxt routing.

## 🛠️ Development
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

For detailed architectural information, see the **[Interactive Workspace Design Doc](file:///d:/self_work/projects/entity_canvas/docs/design_docs/03_interactive_workspace.md)**.
