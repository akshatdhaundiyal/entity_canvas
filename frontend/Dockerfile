# Base stage for dependencies
FROM node:20-slim AS base
WORKDIR /app
COPY package*.json ./
RUN npm install

# Development stage
FROM base AS development
COPY . .
ENV NODE_ENV=development
ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--no-fork"]

# Builder stage for production
FROM base AS builder
COPY . .
ARG NUXT_PUBLIC_API_URL
ENV NUXT_PUBLIC_API_URL=$NUXT_PUBLIC_API_URL
RUN npm run build

# Production stage
FROM node:20-slim AS production
WORKDIR /app
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser
USER appuser
COPY --from=builder --chown=appuser:appgroup /app/.output ./.output
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
