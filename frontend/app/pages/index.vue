<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

useSeoMeta({
  title: 'Entity Canvas — Visual Database Workspace',
  description:
    'Entity Canvas is the modern workspace for database schema exploration. Connect your schema, visualize relations, and build complex queries with drag-and-drop.',
})

const features = [
  {
    title: 'Schema Discovery',
    description: 'Auto-detect tables, columns, foreign keys, and indexes from any connected database in seconds.',
    icon: 'i-heroicons-magnifying-glass-circle',
    bgColor: 'linear-gradient(135deg, #6366f1, #4f46e5)',
  },
  {
    title: 'Visual ER Canvas',
    description: 'Drag entities, draw relations, and explore your data model on a beautiful infinite canvas.',
    icon: 'i-heroicons-squares-2x2',
    bgColor: 'linear-gradient(135deg, #22d3ee, #0891b2)',
  },
  {
    title: 'Query Builder',
    description: 'Build complex SQL queries visually — no syntax memorization required. Export to raw SQL in one click.',
    icon: 'i-heroicons-code-bracket',
    bgColor: 'linear-gradient(135deg, #a78bfa, #7c3aed)',
  },
  {
    title: 'Multi-DB Support',
    description: 'Connect to PostgreSQL, MySQL, SQLite, and more. Unified interface across all your data sources.',
    icon: 'i-heroicons-circle-stack',
    bgColor: 'linear-gradient(135deg, #34d399, #059669)',
  },
  {
    title: 'Team Collaboration',
    description: 'Share canvas views, annotate schemas, and collaborate with your team in real-time.',
    icon: 'i-heroicons-user-group',
    bgColor: 'linear-gradient(135deg, #f472b6, #db2777)',
  },
  {
    title: 'AI Suggestions',
    description: 'Get intelligent query completions and schema improvement suggestions powered by AI.',
    icon: 'i-heroicons-sparkles',
    bgColor: 'linear-gradient(135deg, #fb923c, #ea580c)',
  },
]
</script>

<template>
  <div class="relative isolate overflow-hidden">

    <!-- ── Ambient background blobs ─────────────────────────────── -->
    <div aria-hidden="true" class="pointer-events-none absolute inset-0 -z-10">
      <!-- top-left indigo blob -->
      <div
        class="absolute -top-32 -left-40 h-[600px] w-[600px] rounded-full opacity-20"
        style="background: radial-gradient(circle, #6366f1 0%, transparent 70%); filter: blur(80px);"
      />
      <!-- top-right cyan blob -->
      <div
        class="absolute -top-20 -right-32 h-[480px] w-[480px] rounded-full opacity-15"
        style="background: radial-gradient(circle, #22d3ee 0%, transparent 70%); filter: blur(70px);"
      />
      <!-- bottom blob -->
      <div
        class="absolute -bottom-40 left-1/2 -translate-x-1/2 h-[400px] w-[700px] rounded-full opacity-10"
        style="background: radial-gradient(ellipse, #6366f1 0%, transparent 70%); filter: blur(90px);"
      />
    </div>

    <!-- ── Hero ──────────────────────────────────────────────────── -->
    <UContainer class="pt-24 pb-20 sm:pt-32 sm:pb-28 flex flex-col items-center text-center">

      <!-- badge -->
      <div class="fade-up fade-up-1 inline-flex items-center gap-2 px-3.5 py-1 rounded-full mb-8 text-xs font-semibold text-indigo-300 border border-indigo-500/25" style="background: rgba(99,102,241,0.08);">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
          <span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-400" />
        </span>
        Now in public beta — AI-powered schema discovery
      </div>

      <!-- headline -->
      <h1 class="fade-up fade-up-2 text-5xl sm:text-7xl font-extrabold tracking-tight leading-[1.08] max-w-4xl mb-6">
        <span class="text-white">Your Database,</span><br />
        <span style="background: linear-gradient(135deg, #818cf8 10%, #22d3ee 90%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">
          Beautifully Visual
        </span>
      </h1>

      <!-- sub-headline -->
      <p class="fade-up fade-up-3 text-lg sm:text-xl text-slate-400 max-w-2xl mb-12 leading-relaxed">
        Entity Canvas lets you explore database schemas, map entity relationships,
        and build complex queries — all from an intuitive, drag-and-drop canvas.
      </p>

      <!-- CTAs -->
      <div class="fade-up fade-up-4 flex flex-wrap items-center justify-center gap-4 mb-20">
        <UButton
          to="/app"
          size="xl"
          color="primary"
          label="Start for Free"
          trailing-icon="i-heroicons-arrow-right"
          class="rounded-full px-8 font-semibold"
          style="box-shadow: 0 6px 28px -4px rgba(99,102,241,0.55);"
        />
        <UButton
          to="/docs"
          size="xl"
          color="neutral"
          variant="outline"
          label="Read the Docs"
          leading-icon="i-heroicons-book-open"
          class="rounded-full px-8 font-semibold border-white/10 text-slate-300 hover:border-white/20"
        />
      </div>

      <!-- ── Dashboard preview card ─────────────────────────────── -->
      <div
        class="fade-up fade-up-4 w-full max-w-5xl rounded-2xl p-4 relative group"
        style="background: rgba(248,250,252,0.03); border: 1px solid rgba(255,255,255,0.07); box-shadow: 0 30px 80px -20px rgba(0,0,0,0.6);"
      >
        <!-- inner gradient overlay on hover -->
        <div
          class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"
          style="background: linear-gradient(135deg, rgba(99,102,241,0.06) 0%, transparent 60%);"
        />

        <!-- mock UI chrome -->
        <div
          class="rounded-xl overflow-hidden"
          style="border: 1px solid rgba(255,255,255,0.06); background: #060b1a;"
        >
          <!-- title bar -->
          <div class="flex items-center gap-2 px-4 py-3 border-b border-white/5">
            <span class="h-3 w-3 rounded-full bg-red-500/60" />
            <span class="h-3 w-3 rounded-full bg-yellow-500/60" />
            <span class="h-3 w-3 rounded-full bg-green-500/60" />
            <div class="ml-4 flex-1 h-5 rounded-md" style="background: rgba(255,255,255,0.04); max-width: 280px;" />
          </div>

          <!-- mock panes -->
          <div class="aspect-[16/9] flex" style="min-height: 320px;">
            <!-- sidebar -->
            <div class="w-52 shrink-0 border-r border-white/5 p-3 flex flex-col gap-2">
              <div class="h-6 rounded-md animate-pulse" style="background: rgba(99,102,241,0.15); width: 70%;" />
              <div class="h-4 rounded-md animate-pulse" style="background: rgba(255,255,255,0.05); width: 90%; animation-delay: .1s;" />
              <div class="h-4 rounded-md animate-pulse" style="background: rgba(255,255,255,0.05); width: 75%; animation-delay: .2s;" />
              <div class="h-4 rounded-md animate-pulse" style="background: rgba(255,255,255,0.05); width: 85%; animation-delay: .3s;" />
              <div class="mt-4 h-4 rounded-md animate-pulse" style="background: rgba(34,211,238,0.12); width: 60%; animation-delay: .15s;" />
              <div class="h-4 rounded-md animate-pulse" style="background: rgba(255,255,255,0.05); width: 80%; animation-delay: .25s;" />
              <div class="h-4 rounded-md animate-pulse" style="background: rgba(255,255,255,0.05); width: 65%; animation-delay: .35s;" />
            </div>

            <!-- main canvas area -->
            <div class="flex-1 p-4 relative">
              <!-- floating entity cards -->
              <div class="absolute top-6 left-8 rounded-xl p-3 w-36" style="background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3);">
                <div class="h-3 rounded-sm mb-2 animate-pulse" style="background: #818cf8; width: 60%;" />
                <div class="h-2 rounded-sm mb-1.5 animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.1s;" />
                <div class="h-2 rounded-sm mb-1.5 animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.2s;" />
                <div class="h-2 rounded-sm animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.3s;" />
              </div>
              <div class="absolute top-12 right-16 rounded-xl p-3 w-40" style="background: rgba(34,211,238,0.08); border: 1px solid rgba(34,211,238,0.25);">
                <div class="h-3 rounded-sm mb-2 animate-pulse" style="background: #22d3ee; width: 55%;" />
                <div class="h-2 rounded-sm mb-1.5 animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.15s;" />
                <div class="h-2 rounded-sm mb-1.5 animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.25s;" />
                <div class="h-2 rounded-sm animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.35s;" />
              </div>
              <div class="absolute bottom-10 left-24 rounded-xl p-3 w-32" style="background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.25);">
                <div class="h-3 rounded-sm mb-2 animate-pulse" style="background: #a78bfa; width: 70%;" />
                <div class="h-2 rounded-sm mb-1.5 animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.2s;" />
                <div class="h-2 rounded-sm animate-pulse" style="background: rgba(255,255,255,0.1); animation-delay:.4s;" />
              </div>
              <!-- connecting svg lines -->
              <svg class="absolute inset-0 w-full h-full pointer-events-none" xmlns="http://www.w3.org/2000/svg">
                <line x1="172" y1="60" x2="268" y2="80" stroke="rgba(129,140,248,0.4)" stroke-width="1.5" stroke-dasharray="4 3" />
                <line x1="172" y1="70" x2="156" y2="200" stroke="rgba(167,139,250,0.35)" stroke-width="1.5" stroke-dasharray="4 3" />
              </svg>
            </div>
          </div>
        </div>

        <!-- caption -->
        <p class="mt-3 text-center text-xs text-slate-600">Interactive preview — drag, connect, explore</p>
      </div>
    </UContainer>

    <!-- ── Feature strip ─────────────────────────────────────────── -->
    <section id="features">
      <UContainer class="py-20">
        <div class="text-center mb-14">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Everything you need to understand your data
          </h2>
          <p class="text-slate-400 max-w-xl mx-auto">
            From schema discovery to visual query building — Entity Canvas covers the full workflow.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="group p-6 rounded-2xl transition-all duration-300 hover:-translate-y-1 cursor-default"
            style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);"
          >
            <div
              class="h-11 w-11 rounded-xl flex items-center justify-center mb-4 transition-all duration-300 group-hover:scale-110"
              :style="`background: ${feature.bgColor};`"
            >
              <UIcon :name="feature.icon" class="size-5 text-white" />
            </div>
            <h3 class="text-base font-semibold text-white mb-2">{{ feature.title }}</h3>
            <p class="text-sm text-slate-500 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </UContainer>
    </section>

    <!-- ── Bottom CTA ────────────────────────────────────────────── -->
    <section>
      <UContainer class="py-24 text-center">
        <div
          class="rounded-3xl px-8 py-16 mx-auto max-w-3xl relative overflow-hidden"
          style="background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(34,211,238,0.08) 100%); border: 1px solid rgba(99,102,241,0.25);"
        >
          <div aria-hidden="true" class="absolute -top-16 -right-16 h-64 w-64 rounded-full opacity-20" style="background: radial-gradient(circle, #6366f1, transparent 70%); filter: blur(40px);" />
          <UIcon name="i-heroicons-cube-transparent" class="size-12 mx-auto mb-6 text-indigo-400" />
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to visualize your schema?
          </h2>
          <p class="text-slate-400 mb-8 max-w-md mx-auto">
            Get started in seconds. No credit card required. Works with PostgreSQL, MySQL, SQLite and more.
          </p>
          <UButton
            to="/app"
            size="xl"
            color="primary"
            label="Start for Free"
            trailing-icon="i-heroicons-arrow-right"
            class="rounded-full px-10 font-semibold"
            style="box-shadow: 0 6px 28px -4px rgba(99,102,241,0.55);"
          />
        </div>
      </UContainer>
    </section>

  </div>
</template>


