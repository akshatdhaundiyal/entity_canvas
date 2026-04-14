<script setup lang="ts">
import { useQueryStore } from '~/stores/query'

const store = useQueryStore()

const handleDragStart = (event: DragEvent, column: string) => {
  if (!store.activeTableName) return
  const data = { table: store.activeTableName, column }
  event.dataTransfer?.setData('column', JSON.stringify(data))
}
</script>

<template>
  <div class="space-y-4">
    <div class="px-2 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Columns</div>
    
    <!-- Search Bar -->
    <UInput
      v-if="store.activeTableName"
      v-model="store.columnSearchQuery"
      icon="i-heroicons-magnifying-glass"
      placeholder="Search columns..."
      color="gray"
      variant="outline"
      size="sm"
      :ui="{ rounded: 'rounded-xl' }"
    />

    <!-- Active Table Name Banner -->
    <div v-if="store.activeTableName" class="px-4 py-2 bg-primary-500/5 border border-primary-500/10 rounded-xl flex items-center justify-between">
      <div class="flex items-center gap-2">
        <UIcon name="i-heroicons-table-cells" class="w-3 h-3 text-primary-400" />
        <span class="text-[10px] uppercase font-bold text-primary-400 tracking-wider">{{ store.activeTableName }}</span>
      </div>
      <UButton
        icon="i-heroicons-x-mark"
        color="gray"
        variant="ghost"
        size="2xs"
        @click="store.activeTableName = ''"
      />
    </div>

    <!-- Column List -->
    <div v-if="store.activeTableName" class="space-y-2 max-h-[60vh] overflow-y-auto custom-scrollbar pr-2">
      <div 
        v-for="column in store.filteredColumns" 
        :key="column.name"
        draggable="true"
        @dragstart="handleDragStart($event, column.name)"
        class="px-4 py-3 bg-white/5 border border-transparent rounded-xl hover:border-white/10 hover:bg-white/10 cursor-grab active:cursor-grabbing group transition-all"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-tag" class="w-3.5 h-3.5 text-slate-600 group-hover:text-primary-400 transition-colors" />
            <span class="text-sm text-slate-400 group-hover:text-slate-200 transition-colors">{{ column.name }}</span>
          </div>
          <UBadge size="xs" color="gray" variant="soft" class="font-mono text-[9px] uppercase">
            {{ column.data_type }}
          </UBadge>
        </div>
      </div>

      <!-- Empty Columns State -->
      <div v-if="store.filteredColumns.length === 0" class="text-center py-8 px-4 border border-dashed border-white/5 rounded-2xl">
        <div class="text-slate-600 text-xs italic">No matching columns</div>
      </div>
    </div>

    <!-- No Table Selected State -->
    <div v-else class="text-center py-12 px-6 border-2 border-dashed border-white/5 rounded-3xl opacity-50">
      <div class="mb-4 flex justify-center">
        <div class="p-3 rounded-2xl bg-white/5">
          <UIcon name="i-heroicons-cursor-arrow-rays" class="w-6 h-6 text-slate-600" />
        </div>
      </div>
      <div class="text-slate-500 text-sm font-medium">Select a table</div>
      <div class="text-slate-700 text-[10px] uppercase mt-1">to explore columns</div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  @apply bg-transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-white/5 rounded-full hover:bg-white/10;
}
</style>
