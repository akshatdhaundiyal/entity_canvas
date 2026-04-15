# Knowledge Base 03: DevOps & Deployment Learnings

This document captures the distilled learnings and technical hurdles identified during the setup of the **CI/CD Pipeline** and **Cloud Run** infrastructure.

## Hurdle: GitHub Environment Secret Access
- **Problem**: Deployment jobs failed to pick up `GCP_PROJECT_ID` even though it was defined in the repository.
- **Learning**: GitHub distinguishes between **Repository Secrets** and **Environment Secrets**. Environment secrets can only be accessed if the job explicitly declares the `environment:` it belongs to.
- **Solution**: Added `environment: production` to the `deploy` jobs in both backend and frontend workflows.

## Hurdle: Cloud Run Port Expectations
- **Problem**: The container started successfully but Cloud Run returned: `The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable.`
- **Learning**: Cloud Run injects a `PORT` environment variable (default 8080) and requires the application to listen on that specific port. Hardcoding `8000` causes health check failures.
- **Solution**: Refactored `main:start` to use `os.getenv("PORT", 8000)` and updated the Dockerfile to use the unified entry point.

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
