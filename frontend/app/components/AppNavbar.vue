<template>
  <nav
    class="sticky top-0 z-50 w-full border-b border-white/5"
    style="background: rgba(2, 6, 23, 0.8); backdrop-filter: blur(16px) saturate(1.6);"
  >
    <UContainer>
      <div class="flex h-16 items-center justify-between gap-4">

        <!-- ── Logo ─────────────────────────────────────────────── -->
        <NuxtLink to="/" class="flex items-center gap-2.5 group shrink-0">
          <div
            class="h-8 w-8 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-105 glow-primary"
            style="background: linear-gradient(135deg, #6366f1, #22d3ee);"
          >
            <UIcon name="i-heroicons-cube-transparent" class="size-4 text-white" />
          </div>
          <span
            class="text-[1.05rem] font-bold tracking-tight"
            style="background: linear-gradient(90deg, #fff 40%, rgba(255,255,255,0.5)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;"
          >
            Entity Canvas
          </span>
        </NuxtLink>

        <!-- ── Centre links (desktop) ────────────────────────────── -->
        <div class="hidden md:flex items-center gap-1 flex-1 justify-center">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-3 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all duration-200"
            active-class="text-white bg-white/8"
          >
            {{ link.label }}
          </NuxtLink>
        </div>

        <!-- ── Right actions ─────────────────────────────────────── -->
        <div class="flex items-center gap-2 shrink-0">
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-heroicons-magnifying-glass"
            aria-label="Search"
            class="hidden sm:flex"
          />
          <UButton
            to="/app"
            color="primary"
            variant="solid"
            size="sm"
            label="Launch App"
            trailing-icon="i-heroicons-arrow-right"
            class="rounded-full font-semibold shadow-lg"
            style="box-shadow: 0 4px 20px -4px rgba(99,102,241,0.5);"
          />
        </div>

      </div>
    </UContainer>
  </nav>
</template>

<script setup lang="ts">
const navLinks = [
  { label: 'Features', to: '/#features' },
  { label: 'Documentation', to: '/docs' },
  { label: 'Changelog', to: '/changelog' },
  { label: 'Pricing', to: '/pricing' },
]
</script>
