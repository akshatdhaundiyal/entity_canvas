# Workflow Recipes

## Recipe: Starting the Backend
1.  Ensure the `.venv` is created (`uv sync`).
2.  Run `uv run dev` from the `backend/` directory.
3.  The server will watch for changes and hot-reload.

## Recipe: Adding a New SQL Operator
1.  **Backend Model**: Add the operator to the `Operator` Enum in `backend/models/query.py`.
2.  **Transpiler**: Update the logic in `backend/services/sql_builder.py` to handle the new operator mapping in SQLGlot.
3.  **Frontend State**: Add the operator to the relevant component or store if it needs specific UI handling.
4.  **Verification**: Test an end-to-end query execution with the new operator.
5.  **Documentation**: Update the Knowledge Base or Design Doc if the operator introduces significant changes.

## Recipe: Extending the Query AST
1.  **Design Doc**: Update `docs/design_docs/01_project_scaffolding.md` (or relevant doc) with the AST changes.
2.  **Backend Model**: Update `QueryAST` in `backend/models/query.py`.
3.  **Frontend Store**: Synchronize the `QueryAST` interface in `frontend/stores/query.ts`.
4.  **Transpiler**: Update `build_sql_from_ast` in `backend/services/sql_builder.py`.
5.  **Audit**: Create a Knowledge Base entry in `docs/knowledge_base/` for any hurdles encountered.

## Recipe: Creating a New Milestone
1.  **Summary**: Append a new entry to `00_milestone_summary.md`.
2.  **Design Doc**: Create a new file in `docs/design_docs/XX_feature_name.md`.
3.  **Walkthrough**: Write a functional flow description in the design doc.
4.  **Verification**: Add a Verification Table with test results.
