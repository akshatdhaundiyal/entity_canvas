<script setup lang="ts">
import { useQueryStore } from '~/stores/query'

const store = useQueryStore()
</script>

<template>
  <UCard :ui="{ 
    base: 'overflow-hidden',
    background: 'bg-white/5',
    ring: 'ring-1 ring-white/10',
    divide: 'divide-white/5',
    header: { padding: 'p-0' },
    body: { padding: 'p-0' },
    rounded: 'rounded-3xl'
  }">
    <UTable 
      :rows="store.results" 
      :loading="store.isLoading"
      :ui="{
        wrapper: 'overflow-x-auto custom-scrollbar',
        base: 'min-w-full divide-y divide-white/5',
        thead: 'bg-white/5',
        tr: {
          base: 'hover:bg-white/[0.02] transition-colors'
        },
        th: {
          base: 'text-left rtl:text-right px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider'
        },
        td: {
          base: 'px-4 py-3 text-slate-300 text-sm whitespace-nowrap'
        },
        loadingState: {
          label: 'text-sm text-center text-slate-500 py-12'
        },
        emptyState: {
          label: 'text-sm text-center text-slate-700 italic py-20',
          icon: 'i-heroicons-circle-stack'
        }
      }"
    >
      <template #empty-state>
        <div class="flex flex-col items-center justify-center py-12">
          <UIcon name="i-heroicons-circle-stack" class="w-8 h-8 text-slate-800 mb-2" />
          <span class="text-slate-700 italic text-sm">No results to display. Build and run a query!</span>
        </div>
      </template>
    </UTable>
  </UCard>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  @apply bg-transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-white/5 rounded-full hover:bg-white/10;
}
</style>
