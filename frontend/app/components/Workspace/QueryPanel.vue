<!-- Bottom query results panel -->
<script setup lang="ts">
import { useQueryStore } from '~/stores/query'
import { useWorkspaceStore } from '~/stores/workspace'

const query = useQueryStore()
const ws = useWorkspaceStore()

const isRunning = ref(false)
const executionMs = ref<number | null>(null)
const errorMsg = ref<string | null>(null)
const rows = ref<any[]>([])
const cols = ref<string[]>([])

async function runQuery() {
  isRunning.value = true
  errorMsg.value = null
  executionMs.value = null
  const start = Date.now()

  try {
    // Build typed table list - split is guaranteed to return 'table.col' format
    const tablesRaw = [...new Set(ws.selectedColumns.map(c => c.split('.')[0] ?? ''))]
    const tablesInQuery: string[] = tablesRaw.filter(t => t.length > 0)
    if (tablesInQuery.length === 0) {
      errorMsg.value = 'Select at least one column before running the query.'
      return
    }

    const baseTable = tablesInQuery[0] as string
    query.query.select = ws.chosenColumns.map(({ table, col }) => ({ table: table ?? '', column: col ?? '' }))
    query.query.from = baseTable

    // Auto-construct joins from detected relations
    query.query.joins = []
    for (const t of tablesInQuery.slice(1)) {
      const edge = ws.detectedRelations.find(
        e => (e.fromTable === t && e.toTable === baseTable) ||
             (e.fromTable === baseTable && e.toTable === t)
      )
      if (edge) {
        if (edge.fromTable === t) {
          query.query.joins.push({ table: t, on: `${t}.${edge.fromCol} = ${baseTable}.${edge.toCol}`, type: 'INNER' })
        } else {
          query.query.joins.push({ table: t, on: `${baseTable}.${edge.fromCol} = ${t}.${edge.toCol}`, type: 'INNER' })
        }
      }
    }

    await query.executeQuery()

    executionMs.value = Date.now() - start

    if (query.results?.length > 0) {
      cols.value = Object.keys(query.results[0])
      rows.value = query.results
    } else {
      cols.value = ws.selectedColumns.map(c => c.replace('.', '_'))
      rows.value = []
    }
  } catch (e: any) {
    errorMsg.value = e?.message ?? 'Unknown error'
  } finally {
    isRunning.value = false
  }
}
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">

    <!-- Panel header / toolbar -->
    <div
      class="flex items-center gap-3 px-4 py-2 border-b border-white/5 shrink-0"
      style="background: #0a0f1e;"
    >
      <UIcon name="i-heroicons-table-cells" class="size-4 text-slate-500" />
      <span class="text-xs font-semibold uppercase tracking-widest text-slate-500">Query Results</span>

      <div class="flex-1" />

      <!-- Stats -->
      <template v-if="executionMs !== null && !isRunning">
        <span class="text-[10px] text-slate-600 tabular-nums">
          {{ rows.length }} row{{ rows.length !== 1 ? 's' : '' }}
        </span>
        <span class="h-3 w-px bg-white/10" />
        <span class="text-[10px] text-emerald-500 tabular-nums">
          {{ executionMs }}ms
        </span>
      </template>

      <!-- Run button -->
      <UButton
        size="xs"
        color="primary"
        :loading="isRunning"
        :disabled="ws.selectedColumns.length === 0"
        icon="i-heroicons-play"
        label="Run Query"
        class="rounded-full"
        style="box-shadow: 0 2px 12px -2px rgba(99,102,241,0.4);"
        @click="runQuery"
      />
    </div>

    <!-- Error state -->
    <div v-if="errorMsg" class="px-4 py-3 shrink-0">
      <UAlert
        color="error"
        variant="subtle"
        icon="i-heroicons-exclamation-circle"
        :title="errorMsg"
        class="text-xs"
      />
    </div>

    <!-- Empty / prompt state -->
    <div
      v-if="rows.length === 0 && !isRunning && !errorMsg"
      class="flex-1 flex flex-col items-center justify-center gap-2 text-slate-700"
    >
      <UIcon name="i-heroicons-play-circle" class="size-8 opacity-40" />
      <p class="text-xs">
        {{ ws.selectedColumns.length === 0 ? 'Select columns, then run the query.' : 'Click Run Query to execute.' }}
      </p>
    </div>

    <!-- Loading -->
    <div v-else-if="isRunning" class="flex-1 flex items-center justify-center gap-2 text-slate-500">
      <UIcon name="i-heroicons-arrow-path" class="size-5 animate-spin text-indigo-400" />
      <span class="text-xs">Executing…</span>
    </div>

    <!-- Results table -->
    <div v-else-if="rows.length > 0" class="flex-1 overflow-auto">
      <table class="w-full text-xs text-left border-collapse">
        <thead class="sticky top-0 z-10" style="background: #0a0f1e;">
          <tr>
            <th
              class="px-2 py-2 border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-slate-500 w-8 text-right"
            >#</th>
            <th
              v-for="col in cols"
              :key="col"
              class="px-3 py-2 border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-slate-500 whitespace-nowrap"
            >{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, ri) in rows"
            :key="ri"
            class="border-b border-white/[0.03] hover:bg-white/[0.025] transition-colors"
          >
            <td class="px-2 py-1.5 text-slate-700 text-right tabular-nums">{{ ri + 1 }}</td>
            <td
              v-for="col in cols"
              :key="col"
              class="px-3 py-1.5 text-slate-300 whitespace-nowrap font-mono"
            >
              <span v-if="row[col] === null || row[col] === undefined" class="text-slate-700 italic">null</span>
              <span v-else>{{ row[col] }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>
