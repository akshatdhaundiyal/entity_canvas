# Lesson Learned: Postgres 17 & Docker SSR Networking

## The Hurdle
Two major technical blocks occurred during the containerization of Entity Canvas:
1. **SQL Syntax Errors**: The Pagila dump used generated columns but omitted the `STORED` keyword, which is mandatory in modern Postgres.
2. **SSR Connectivity 500s**: In Nuxt, server-side fetches happen *inside* the Docker network, while client-side fetches happen *outside* in the browser. Using a single URL for both causes one to fail.

## The Solution

### 1. Postgres 17 Patching
When migrating older SQL dumps to PG17, ensure generated columns are declared as:
```sql
column_name TYPE GENERATED ALWAYS AS (expression) STORED
```

### 2. Dual-Base-URL Pattern
Instead of a proxy, use a smart toggle in the Pinia store:
```typescript
const apiBase = import.meta.server 
  ? config.apiBase           // http://backend:8080 (Internal)
  : config.public.apiBase    // http://localhost:8000 (External)
```

## Why this is a "Permanent Lesson"
This pattern is mandatory for any Dockerized SSR application. It prevents "Network Gap" errors and ensures that private backend keys are never leaked to the client while maintaining high performance for internal fetches.
