<script setup lang="ts">
import { useQueryStore } from '~/stores/query'

const props = defineProps<{
  title: string
  zone: 'select' | 'filter'
}>()

const store = useQueryStore()

const handleDrop = (event: DragEvent) => {
  const data = event.dataTransfer?.getData('column')
  if (data) {
    const { table, column } = JSON.parse(data)
    if (props.zone === 'select') {
      store.addColumn(table, column)
    } else {
      store.addFilter(column)
    }
  }
}

const operators = ['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'ILIKE', 'IN', 'IS NULL']
</script>

<template>
  <div 
    @dragover.prevent 
    @drop.prevent="handleDrop"
    class="flex-1"
  >
    <UCard :ui="{ 
      base: 'h-full transition-all border-dashed border-2',
      background: 'bg-white/5',
      ring: '',
      divide: '',
      header: { padding: 'p-4' },
      body: { padding: 'p-4' },
      rounded: 'rounded-3xl'
    }">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon :name="zone === 'select' ? 'i-heroicons-squares-plus' : 'i-heroicons-funnel'" class="w-4 h-4 text-primary-400" />
            <span class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">{{ title }}</span>
          </div>
          <div class="h-1.5 w-1.5 rounded-full bg-primary-500 animate-pulse"></div>
        </div>
      </template>

      <div v-if="zone === 'select'" class="flex flex-wrap gap-2">
        <div 
          v-for="(col, index) in store.query.select" 
          :key="index"
          class="flex items-center gap-1.5 pl-1 pr-1 py-1 rounded-xl bg-primary-500/10 border border-primary-500/20 group/item"
        >
          <UBadge variant="soft" size="xs" color="primary" class="font-mono text-[9px]">{{ col.table }}</UBadge>
          <span class="text-xs font-medium text-slate-200">{{ col.column }}</span>
          <UButton
            icon="i-heroicons-x-mark"
            color="gray"
            variant="ghost"
            size="2xs"
            class="opacity-50 hover:opacity-100"
            @click="store.removeColumn(index)"
          />
        </div>
        
        <div v-if="store.query.select.length === 0" class="w-full flex flex-col items-center justify-center py-8 opacity-40">
          <UIcon name="i-heroicons-cursor-arrow-ripple" class="w-8 h-8 mb-2" />
          <span class="text-[10px] uppercase tracking-widest font-bold">Drop columns here</span>
        </div>
      </div>

      <div v-else class="space-y-3">
        <div 
          v-for="(filter, index) in store.query.where" 
          :key="index"
          class="flex gap-2 items-center p-2 rounded-2xl bg-white/5 border border-white/5"
        >
          <div class="min-w-0 flex-1 flex items-center gap-2 text-xs text-slate-400 truncate pl-1">
            <UIcon name="i-heroicons-tag" class="w-3 h-3" />
            {{ filter.column }}
          </div>
          <USelect
            v-model="filter.operator"
            :options="operators"
            size="2xs"
            color="gray"
            variant="ghost"
            class="w-20"
          />
          <UInput
            v-model="filter.value"
            placeholder="Value"
            size="2xs"
            color="gray"
            variant="outline"
            class="flex-1"
          />
        </div>

        <div v-if="store.query.where.length === 0" class="w-full flex flex-col items-center justify-center py-8 opacity-40">
          <UIcon name="i-heroicons-funnel" class="w-8 h-8 mb-2" />
          <span class="text-[10px] uppercase tracking-widest font-bold">Add filters here</span>
        </div>
      </div>
    </UCard>
  </div>
</template>
