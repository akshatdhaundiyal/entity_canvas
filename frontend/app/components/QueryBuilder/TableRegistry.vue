<script setup lang="ts">
import { useQueryStore } from '~/stores/query'

const store = useQueryStore()

const selectTable = (name: string) => {
  store.activeTableName = name
}
</script>

<template>
  <div class="space-y-4">
    <div class="px-2 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Tables</div>
    
    <!-- Search Bar -->
    <UInput
      v-model="store.tableSearchQuery"
      icon="i-heroicons-magnifying-glass"
      placeholder="Search tables..."
      color="gray"
      variant="outline"
      size="sm"
      :ui="{ rounded: 'rounded-xl' }"
    />

    <!-- Table List -->
    <div class="space-y-1">
      <div 
        v-for="table in store.filteredTables" 
        :key="table.name" 
        @click="selectTable(table.name)"
        :class="[
          'px-4 py-3 rounded-xl cursor-pointer transition-all border flex items-center gap-3 group',
          store.activeTableName === table.name 
            ? 'bg-primary-500/10 border-primary-500/30' 
            : 'bg-white/5 border-transparent hover:bg-white/10 hover:border-white/10'
        ]"
      >
        <UIcon 
          :name="store.activeTableName === table.name ? 'i-heroicons-table-cells-20-solid' : 'i-heroicons-table-cells'" 
          :class="[
            'w-4 h-4 transition-colors',
            store.activeTableName === table.name ? 'text-primary-400' : 'text-slate-500 group-hover:text-slate-300'
          ]"
        />
        <span 
          :class="[
            'text-sm font-medium transition-colors',
            store.activeTableName === table.name ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'
          ]"
        >
          {{ table.name }}
        </span>
      </div>

      <!-- Empty State -->
      <div v-if="store.filteredTables.length === 0" class="text-center py-8 px-4 border border-dashed border-white/5 rounded-2xl">
        <div class="text-slate-600 text-xs italic">No tables found</div>
      </div>
    </div>
  </div>
</template>
