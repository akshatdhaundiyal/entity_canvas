# Knowledge Base 03: DevOps & Deployment Learnings

This document captures the distilled learnings and technical hurdles identified during the setup of the **CI/CD Pipeline** and **Cloud Run** infrastructure.

## Hurdle: GitHub Environment Secret Access
- **Problem**: Deployment jobs failed to pick up `GCP_PROJECT_ID` even though it was defined in the repository.
- **Learning**: GitHub distinguishes between **Repository Secrets** and **Environment Secrets**. Environment secrets can only be accessed if the job explicitly declares the `environment:` it belongs to.
- **Solution**: Added `environment: production` to the `deploy` jobs in both backend and frontend workflows.

## Decision: Multi-Stage Frontend Dockerfile
- **Context**: The initial Nuxt Docker image was over 800MB due to node_modules and dev dependencies remaining in the final image.
- **Learning**: Nuxt (with Nitro) generates a standalone `.output` folder that requires very few runtime dependencies.
- **Solution**: Implemented a multi-stage build.
  - *Stage 1*: Build.
  - *Stage 2*: Copy `.output` only.
- **Impact**: Final image size reduced from ~800MB to ~150MB.

## Hurdle: Chained Workflow Triggers
- **Problem**: The frontend needs the backend's URL to communicate, but Cloud Run URLs can change (though unlikely).
- **Learning**: Using `workflow_run` with `types: [completed]` allows the frontend to wait for the backend to be successfully healthy before attempting to fetch its URL and deploy.
- **Benefit**: Ensures the frontend always points to the live, current backend service without manual configuration.

---

## Technical Definitions

| Term | Definition |
|------|------------|
| **Serverless** | A cloud-computing execution model where the cloud provider runs the server and dynamically manages the allocation of machine resources. |
| **Artifact Registry** | A fully managed service that allows you to store, manage, and secure your Docker images in Google Cloud. |
| **IAM (GCP)** | Identity and Access Management; a framework of policies and technologies to ensure that the right users have the appropriate access to technology resources. |

> [!CAUTION]
> **Service Account Keys**: Never check your `GCP_CREDENTIALS` JSON file into the repository. Always manage them via GitHub Repository Secrets.
