<template>
  <nav
    class="z-50 w-full border-b border-white/5 h-14 flex items-center px-4 justify-between shrink-0"
    style="background: #060c1a;"
  >
    <!-- ── Left: Logo & Context ────────────────────────────── -->
    <div class="flex items-center gap-4">
      <NuxtLink to="/" class="flex items-center gap-2 group">
        <div
          class="h-7 w-7 rounded-lg flex items-center justify-center transition-transform duration-200 group-hover:scale-105"
          style="background: linear-gradient(135deg, #6366f1, #22d3ee);"
        >
          <UIcon name="i-heroicons-cube-transparent" class="size-4 text-white" />
        </div>
        <span class="text-sm font-bold tracking-tight text-white/90">
          Entity Canvas
        </span>
      </NuxtLink>

      <div class="h-4 w-px bg-white/10 mx-1" />
      
      <span class="text-xs font-medium text-slate-500 uppercase tracking-widest">Workspace</span>
    </div>

    <!-- ── Centre: Workspace Metrics ─────────────────────────── -->
    <div class="hidden md:flex items-center gap-6 text-[11px] font-medium text-slate-500 uppercase tracking-wider">
      <div class="flex items-center gap-2">
        <span class="text-indigo-400">{{ ws.selectedTableNames.length }}</span>
        <span>Tables Selected</span>
      </div>
      <div class="h-3 w-px bg-white/10" />
      <div class="flex items-center gap-2">
        <span class="text-indigo-400">{{ ws.selectedColumns.length }}</span>
        <span>Columns Selected</span>
      </div>
    </div>

    <!-- ── Right: Tooling ───────────────────────────────────── -->
    <div class="flex items-center gap-3">
      <UButton
        size="xs"
        color="neutral"
        variant="ghost"
        icon="i-heroicons-arrow-path"
        :loading="query.isLoading"
        title="Refresh schema"
        @click="query.fetchSchema()"
      />

      <div class="h-4 w-px bg-white/10 mx-1" />

      <DatabaseSwitcher />
      
      <div class="h-4 w-px bg-white/10 mx-1" />

      <UButton
        color="neutral"
        variant="ghost"
        class="p-0.5 rounded-full ring-1 ring-white/10 hover:ring-indigo-500/50 transition-all"
      >
        <UAvatar
          src="https://github.com/nutlope.png"
          alt="Avatar"
          size="xs"
        />
      </UButton>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useWorkspaceStore } from '~/stores/workspace'
import { useQueryStore } from '~/stores/query'

const ws = useWorkspaceStore()
const query = useQueryStore()
</script>
