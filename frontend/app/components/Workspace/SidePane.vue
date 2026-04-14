<!-- Left content pane — renders tab-specific content -->
<script setup lang="ts">
import { useQueryStore } from '~/stores/query'
import { useWorkspaceStore } from '~/stores/workspace'

const query = useQueryStore()
const ws = useWorkspaceStore()

// Group cascaded columns by table for display
const cascadedGrouped = computed(() => {
  const groups: Record<string, typeof ws.cascadedColumns> = {}
  for (const item of ws.cascadedColumns) {
    if (!groups[item.table]) groups[item.table] = []
    groups[item.table]!.push(item)
  }
  return groups
})

// Simple SQL token coloriser (no external deps)
function tokeniseSql(sql: string) {
  const keywords = /\b(SELECT|FROM|JOIN|ON|WHERE|LIMIT|AND|OR|LEFT|INNER|RIGHT|GROUP BY|ORDER BY|HAVING|AS)\b/gi
  const nums = /\b\d+\b/g
  const punctuation = /[,;]/g
  return sql
    .replace(keywords, m => `<span class="sql-kw">${m}</span>`)
    .replace(nums, m => `<span class="sql-num">${m}</span>`)
    .replace(punctuation, m => `<span class="sql-punct">${m}</span>`)
}

const highlightedSQL = computed(() => tokeniseSql(ws.generatedSQL))

function copySQL() {
  navigator.clipboard?.writeText(ws.generatedSQL)
}
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">

    <!-- Pane header -->
    <div class="px-4 py-3 border-b border-white/5 shrink-0 flex items-center justify-between">
      <h3 class="text-xs font-semibold uppercase tracking-widest text-slate-500">
        <template v-if="ws.activeTab === 'tables'">Schema Tables</template>
        <template v-else-if="ws.activeTab === 'cascaded'">Cascaded Columns</template>
        <template v-else-if="ws.activeTab === 'selected'">Selected Columns</template>
        <template v-else-if="ws.activeTab === 'filters'">Filters</template>
        <template v-else-if="ws.activeTab === 'sql'">Generated SQL</template>
      </h3>

      <!-- Limit input -->
      <div class="flex items-center gap-2">
        <span class="text-[10px] text-slate-600">LIMIT</span>
        <input
          v-model="ws.limit"
          type="number"
          class="w-12 bg-white/5 border border-white/10 rounded px-1 py-0.5 text-[10px] text-slate-300 focus:outline-none focus:border-indigo-500"
        />
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="query.isLoading" class="flex-1 flex items-center justify-center">
      <div class="flex flex-col items-center gap-3 text-slate-500">
        <UIcon name="i-heroicons-arrow-path" class="size-6 animate-spin text-indigo-400" />
        <span class="text-xs">Loading schema…</span>
      </div>
    </div>

    <!-- Error state -->
    <div v-else-if="query.error" class="flex-1 flex items-start p-4">
      <UAlert
        color="error"
        variant="subtle"
        icon="i-heroicons-exclamation-triangle"
        :title="query.error"
        class="text-xs"
      />
    </div>

    <!-- ── TABLES TAB ─────────────────────────────────────────────── -->
    <div v-else-if="ws.activeTab === 'tables'" class="flex-1 overflow-y-auto">
      <div v-if="query.availableTables.length === 0" class="px-4 py-8 text-center text-xs text-slate-600">
        No tables found in schema.
      </div>

      <div
        v-for="table in query.availableTables"
        :key="table.name"
        class="group border-b border-white/[0.04] last:border-0"
      >
        <!-- Table row -->
        <label
          class="flex items-center gap-3 px-4 py-2.5 cursor-pointer hover:bg-white/[0.03] transition-colors"
        >
          <input
            type="checkbox"
            class="sr-only"
            :checked="ws.isTableSelected(table.name)"
            @change="ws.toggleTable(table.name)"
          />
          <!-- Colour dot / checkbox indicator -->
          <div
            class="h-4 w-4 rounded-sm shrink-0 flex items-center justify-center border transition-all"
            :style="ws.isTableSelected(table.name)
              ? `background: ${ws.tableColor(table.name)}; border-color: ${ws.tableColor(table.name)};`
              : 'border-color: rgba(255,255,255,0.12);'"
          >
            <UIcon v-if="ws.isTableSelected(table.name)" name="i-heroicons-check" class="size-2.5 text-white" />
          </div>

          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-slate-200 truncate">{{ table.name }}</p>
            <p class="text-[10px] text-slate-600">{{ table.columns.length }} columns</p>
          </div>

          <div
            class="h-5 w-1 rounded-full shrink-0 transition-all"
            :style="`background: ${ws.tableColor(table.name)}; opacity: ${ws.isTableSelected(table.name) ? '1' : '0.2'};`"
          />
        </label>

        <!-- Expanded column preview when selected -->
        <div
          v-if="ws.isTableSelected(table.name)"
          class="pb-2 overflow-hidden"
        >
          <div
            v-for="col in table.columns"
            :key="col.name"
            class="flex items-center gap-2 pl-10 pr-4 py-0.5"
          >
            <div
              class="h-1.5 w-1.5 rounded-full shrink-0"
              :style="`background: ${ws.tableColor(table.name)}66;`"
            />
            <span class="text-xs text-slate-400 font-mono truncate">{{ col.name }}</span>
            <span class="ml-auto text-[10px] text-slate-600 shrink-0">{{ col.data_type }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── CASCADED COLUMNS TAB ───────────────────────────────────── -->
    <div v-else-if="ws.activeTab === 'cascaded'" class="flex-1 overflow-y-auto">
      <div v-if="Object.keys(cascadedGrouped).length === 0" class="px-4 py-8 text-center text-xs text-slate-600">
        Select tables to see cascaded columns.
      </div>

      <div
        v-for="(cols, tableName) in cascadedGrouped"
        :key="tableName"
      >
        <!-- Table group header -->
        <div
          class="sticky top-0 flex items-center gap-2 px-4 py-1.5 border-b border-white/5 z-10"
          style="background: #0a0f1e;"
        >
          <div
            class="h-2.5 w-2.5 rounded-sm"
            :style="`background: ${ws.tableColor(tableName)};`"
          />
          <span class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
            {{ tableName }}
          </span>
          <span
            v-if="cols[0]?.cascaded"
            class="ml-auto text-[9px] px-1.5 py-0.5 rounded-full text-slate-500 border border-white/10"
          >
            cascaded
          </span>
        </div>

        <!-- Columns -->
        <label
          v-for="col in cols"
          :key="`${col.table}.${col.col}`"
          class="flex items-center gap-3 px-4 py-2 cursor-pointer hover:bg-white/[0.03] transition-colors"
        >
          <div
            class="h-3.5 w-3.5 rounded-sm shrink-0 flex items-center justify-center border transition-all"
            :style="ws.isColumnSelected(`${col.table}.${col.col}`)
              ? `background: ${ws.tableColor(col.table)}; border-color: ${ws.tableColor(col.table)};`
              : 'border-color: rgba(255,255,255,0.12);'"
            @click="ws.toggleColumn(`${col.table}.${col.col}`)"
          >
            <UIcon v-if="ws.isColumnSelected(`${col.table}.${col.col}`)" name="i-heroicons-check" class="size-2 text-white" />
          </div>
          <span class="text-xs font-mono text-slate-300 truncate flex-1">{{ col.col }}</span>
          <span class="text-[10px] text-slate-600 shrink-0">{{ col.type }}</span>
        </label>
      </div>
    </div>

    <!-- ── SELECTED COLUMNS TAB ───────────────────────────────────── -->
    <div v-else-if="ws.activeTab === 'selected'" class="flex-1 overflow-y-auto">
      <div v-if="ws.selectedColumns.length === 0" class="px-4 py-8 text-center text-xs text-slate-600">
        No columns selected yet. Choose from the Cascaded tab.
      </div>

      <div
        v-for="(tc, i) in ws.selectedColumns"
        :key="tc"
        class="flex items-center gap-3 px-4 py-2.5 border-b border-white/[0.04] last:border-0 group hover:bg-white/[0.03] transition-colors"
      >
        <!-- Order number -->
        <span class="text-[10px] text-slate-600 w-4 text-right shrink-0">{{ i + 1 }}</span>

        <!-- Colour dot -->
        <div
          class="h-2 w-2 rounded-full shrink-0"
          :style="`background: ${ws.tableColor(tc.split('.')[0] ?? '')};`"
        />

        <div class="min-w-0 flex-1">
          <span class="text-[10px] text-slate-600 leading-none">{{ tc.split('.')[0] }}.</span>
          <span class="text-xs font-mono text-slate-300 leading-none block">{{ tc.split('.')[1] }}</span>
        </div>

        <!-- Sort toggle -->
        <button
          class="p-1 rounded hover:bg-white/10 transition-colors shrink-0"
          :class="ws.sorts.find(s => s.column === tc) ? 'text-indigo-400' : 'text-slate-600'"
          @click="ws.toggleSort(tc)"
        >
          <UIcon 
            :name="ws.sorts.find(s => s.column === tc)?.direction === 'DESC' ? 'i-heroicons-bars-arrow-down' : 'i-heroicons-bars-arrow-up'" 
            class="size-3.5"
          />
        </button>

        <!-- Filter shortcut -->
        <button
          class="p-1 rounded hover:bg-white/10 text-slate-600 hover:text-indigo-400 transition-colors shrink-0"
          @click="ws.addFilter(tc)"
        >
          <UIcon name="i-heroicons-funnel" class="size-3.5" />
        </button>

        <!-- Move up/down -->
        <div class="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            v-if="i > 0"
            class="p-0.5 text-slate-500 hover:text-white"
            @click="ws.moveColumn(i, i - 1)"
          >
            <UIcon name="i-heroicons-chevron-up" class="size-3" />
          </button>
          <button
            v-if="i < ws.selectedColumns.length - 1"
            class="p-0.5 text-slate-500 hover:text-white"
            @click="ws.moveColumn(i, i + 1)"
          >
            <UIcon name="i-heroicons-chevron-down" class="size-3" />
          </button>
        </div>

        <!-- Remove -->
        <button
          class="p-0.5 text-slate-600 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100"
          @click="ws.toggleColumn(tc)"
        >
          <UIcon name="i-heroicons-x-mark" class="size-3" />
        </button>
      </div>

      <!-- Summary -->
      <div v-if="ws.selectedColumns.length > 0" class="px-4 py-3 border-t border-white/5 text-[10px] text-slate-600">
        {{ ws.selectedColumns.length }} column{{ ws.selectedColumns.length !== 1 ? 's' : '' }} selected
        <span v-if="ws.sorts.length > 0"> • {{ ws.sorts.length }} sorted</span>
      </div>
    </div>

    <!-- ── FILTERS TAB ─────────────────────────────────────────── -->
    <div v-else-if="ws.activeTab === 'filters'" class="flex-1 overflow-y-auto p-4 space-y-4">
      <div v-if="ws.filters.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
        <UIcon name="i-heroicons-funnel" class="size-8 text-slate-700 mb-2" />
        <p class="text-xs text-slate-600 max-w-[180px]">No filters applied. Use the funnel icon next to selected columns to add one.</p>
      </div>

      <div
        v-for="(f, fi) in ws.filters"
        :key="fi"
        class="bg-white/[0.03] border border-white/5 rounded-lg p-3 space-y-2 relative group"
      >
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-mono text-indigo-400">{{ f.column }}</span>
          <button 
            class="p-1 text-slate-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
            @click="ws.removeFilter(fi)"
          >
            <UIcon name="i-heroicons-trash" class="size-3" />
          </button>
        </div>

        <div class="flex gap-2">
          <select 
            v-model="f.operator"
            class="bg-white/5 border border-white/10 rounded px-1.5 py-1 text-xs text-slate-300 focus:outline-none"
          >
            <option value="=">=</option>
            <option value="!=">!=</option>
            <option value=">">></option>
            <option value="<"><</option>
            <option value="LIKE">LIKE</option>
          </select>

          <input 
            v-model="f.value"
            placeholder="Value..."
            class="flex-1 bg-white/5 border border-white/10 rounded px-2 py-1 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <!-- Logic selector if not first -->
        <div v-if="fi > 0" class="absolute -top-3 left-1/2 -translate-x-1/2">
          <select 
            v-model="f.logic"
            class="bg-slate-900 border border-white/10 rounded px-1 text-[9px] text-slate-500 font-bold uppercase"
          >
            <option value="AND">AND</option>
            <option value="OR">OR</option>
          </select>
        </div>
      </div>

      <div v-if="ws.filters.length > 0" class="pt-4 border-t border-white/5">
        <p class="text-[10px] text-slate-600 italic text-center">
          Filters are applied in order. Logic (AND/OR) connects each filter to the previous one.
        </p>
      </div>
    </div>

    <!-- ── SQL TAB ─────────────────────────────────────────────────── -->
    <div v-else-if="ws.activeTab === 'sql'" class="flex-1 overflow-y-auto">
      <div class="p-4">
        <!-- Copy button -->
        <div class="flex justify-end mb-2">
          <UButton
            size="xs"
            color="neutral"
            variant="ghost"
            icon="i-heroicons-clipboard-document"
            label="Copy"
            @click="copySQL"
          />
        </div>

        <!-- Syntax-highlighted block -->
        <!-- eslint-disable-next-line vue/no-v-html -->
        <pre
          class="sql-block text-xs font-mono leading-6 whitespace-pre-wrap rounded-xl p-4 overflow-x-auto"
          style="background: #070d1a; border: 1px solid rgba(255,255,255,0.06);"
          v-html="highlightedSQL"
        />
      </div>
    </div>

  </div>
</template>

<style scoped>
.sql-block :deep(.sql-kw)    { color: #818cf8; font-weight: 600; }
.sql-block :deep(.sql-num)   { color: #34d399; }
.sql-block :deep(.sql-punct) { color: #94a3b8; }
</style>
