# Knowledge Base 03: DevOps & Deployment Learnings

This document captures the distilled learnings and technical hurdles identified during the setup of the **CI/CD Pipeline** and **Cloud Run** infrastructure.

## Decision: System-Wide Dependency Installation
- **Problem**: Containerized virtual environments (e.g., `/app/.venv`) often lead to binary permission issues and module discovery failures when running as a non-root user.
- **Learning**: Installing dependencies into the system site-packages (`uv sync --system`) simplifies the environment path and accessibility for all users within the container.
- **Solution**: Performed `uv sync --system` as root during build, then switched to `appuser` for execution.

## Hurdle: Cloud Run Port Substitution
- **Context**: Passing the dynamic `$PORT` from Cloud Run to a Python entry point can be fragile if handled only in application code.
- **Solution**: Adopting the shell-form `CMD` (e.g., `CMD uvicorn ... --port ${PORT}`) allows the container runtime to perform the substitution natively.

## Decision: Unified CI/CD Pipeline Lifecycle
- **Context**: Separate workflows (`deploy-backend`, `deploy-frontend`) led to synchronization issues and "Service Not Found" errors due to missing project context.
- **Learning**: Sequential execution in a single job (`deploy.yml`) ensures the backend URL is fetched and injected into the frontend build in one atomic process.
- **Benefit**: Reduced deployment complexity and guaranteed consistency between service versions.

## Refined: Explicit Project Context
- **Hurdle**: `gcloud run services describe` repeatedly failed with `Cannot find service [entity-canvas-backend]`.
- **Solution**: Added `--project ${{ secrets.GCP_PROJECT_ID }}` to all `gcloud` commands to ensure the correct project context is maintained across GitHub Runner environments.

## Iteration: Multi-Stage Frontend Dockerfile
- **Context**: The initial Nuxt Docker image was over 800MB due to node_modules and dev dependencies remaining in the final image.
- **Learning**: Nuxt (with Nitro) generates a standalone `.output` folder that requires very few runtime dependencies.
- **Solution**: Implemented a multi-stage build.
  - *Stage 1*: Build.
  - *Stage 2*: Copy `.output` only.
- **Impact**: Final image size reduced from ~800MB to ~150MB.

---

## Technical Definitions

| Term | Definition |
|------|------------|
| **Serverless** | A cloud-computing execution model where the cloud provider runs the server and dynamically manages the allocation of machine resources. |
| **Artifact Registry** | A fully managed service that allows you to store, manage, and secure your Docker images in Google Cloud. |
| **IAM (GCP)** | Identity and Access Management; a framework of policies and technologies to ensure that the right users have the appropriate access to technology resources. |

> [!CAUTION]
> **Service Account Keys**: Never check your `GCP_CREDENTIALS` JSON file into the repository. Always manage them via GitHub Repository Secrets.
