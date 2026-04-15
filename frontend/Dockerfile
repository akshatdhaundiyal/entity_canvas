# Stage 1: Build
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install

# Build application
ARG NUXT_PUBLIC_API_URL
ENV NUXT_PUBLIC_API_URL=$NUXT_PUBLIC_API_URL

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser
WORKDIR /app
RUN chown appuser:appgroup /app

# Switch to non-root user
USER appuser

# Only copy the essential output from the builder stage
COPY --from=builder --chown=appuser:appgroup /app/.output ./.output

# Set production environment
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

# Expose Nuxt port
EXPOSE 3000

# Start Nuxt server
CMD ["node", ".output/server/index.mjs"]
