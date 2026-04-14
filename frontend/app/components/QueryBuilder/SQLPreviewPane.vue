<script setup lang="ts">
import { ref } from 'vue'
import { useQueryStore } from '~/stores/query'

const store = useQueryStore()
const copied = ref(false)

const formatSQL = (sql: string) => {
  if (!sql) return ''
  return sql
    .replace(/\b(SELECT|FROM|JOIN|LEFT|INNER|WHERE|ON|AND|OR|AS)\b/g, '<span class="text-primary-400 font-bold">$1</span>')
}

const copyToClipboard = () => {
  if (!store.sql) return
  navigator.clipboard.writeText(store.sql)
  copied.value = true
  setTimeout(() => copied.value = false, 2000)
}
</script>

<template>
  <div class="h-full flex flex-col space-y-4">
    <div class="px-2 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">SQL Preview</div>
    
    <UCard :ui="{ 
      base: 'flex-1 overflow-hidden relative group h-full',
      background: 'bg-white/5',
      ring: 'ring-1 ring-white/10',
      divide: '',
      body: { padding: 'p-6 h-full' },
      rounded: 'rounded-3xl'
    }">
      <div class="absolute top-4 right-4 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
        <UButton
          :icon="copied ? 'i-heroicons-check' : 'i-heroicons-clipboard-document'"
          :color="copied ? 'green' : 'gray'"
          variant="ghost"
          size="xs"
          @click="copyToClipboard"
        >
          {{ copied ? 'Copied!' : 'Copy' }}
        </UButton>
      </div>

      <div class="absolute top-4 left-4 text-[9px] uppercase text-slate-700 font-mono tracking-widest">postgres_dialect.v1</div>

      <div class="mt-8 h-full overflow-auto custom-scrollbar">
        <div class="text-slate-700 text-[11px] font-mono mb-3">// Generated Query</div>
        <div v-if="store.sql" v-html="formatSQL(store.sql)" class="font-mono text-xs leading-relaxed whitespace-pre-wrap text-slate-300"></div>
        <div v-else class="text-slate-800 italic text-xs mt-4">Drafting query...</div>
      </div>
      
      <!-- Ambient Glow -->
      <div class="absolute -bottom-12 -right-12 h-24 w-24 bg-primary-500/5 rounded-full blur-3xl pointer-events-none"></div>
    </UCard>
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
