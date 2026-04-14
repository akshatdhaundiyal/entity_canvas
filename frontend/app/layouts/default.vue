<template>
  <!-- Default layout: navbar + page content + footer -->
  <div class="min-h-screen flex flex-col" style="background-color: #020617; color: #f1f5f9;">
    <AppNavbar />

    <main class="flex-1">
      <slot />
    </main>

    <footer class="border-t border-white/5 py-10">
      <UContainer>
        <div class="flex flex-col md:flex-row items-center justify-between gap-6">
          <!-- Brand -->
          <div class="flex items-center gap-2">
            <div
              class="h-7 w-7 rounded-lg flex items-center justify-center"
              style="background: linear-gradient(135deg, #6366f1, #22d3ee);"
            >
              <UIcon name="i-heroicons-cube-transparent" class="size-4 text-white" />
            </div>
            <span class="text-sm font-semibold text-slate-300">Entity Canvas</span>
          </div>

          <!-- Links -->
          <nav class="flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
            <NuxtLink
              v-for="link in footerLinks"
              :key="link.to"
              :to="link.to"
              class="text-xs text-slate-500 hover:text-slate-300 transition-colors"
            >
              {{ link.label }}
            </NuxtLink>
          </nav>

          <!-- Copyright -->
          <p class="text-xs text-slate-600">
            &copy; {{ year }} Entity Canvas. All rights reserved.
          </p>
        </div>
      </UContainer>
    </footer>
  </div>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()

const footerLinks = [
  { label: 'Privacy', to: '/privacy' },
  { label: 'Terms', to: '/terms' },
  { label: 'Documentation', to: '/docs' },
  { label: 'Status', to: '/status' },
]
</script>
