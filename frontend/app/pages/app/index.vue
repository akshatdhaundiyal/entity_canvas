<script setup lang="ts">
import { useQueryStore } from '~/stores/query'
import { useWorkspaceStore, type WorkspaceTab } from '~/stores/workspace'

definePageMeta({ layout: 'app' })

useSeoMeta({
  title: 'Workspace — Entity Canvas',
  description: 'Explore your database schema, build visual ER diagrams, and run queries.',
})

const query = useQueryStore()
const ws = useWorkspaceStore()

// Fetch schema on mount
onMounted(() => query.fetchSchema())

// ── Sidebar tab definitions ────────────────────────────────────
const tabs: { id: WorkspaceTab; icon: string; label: string }[] = [
  { id: 'tables',   icon: 'i-heroicons-table-cells',         label: 'Tables'   },
  { id: 'cascaded', icon: 'i-heroicons-arrows-right-left',   label: 'Cascaded' },
  { id: 'selected', icon: 'i-heroicons-check-circle',        label: 'Selected' },
  { id: 'filters',  icon: 'i-heroicons-funnel',              label: 'Filters'  },
  { id: 'sql',      icon: 'i-heroicons-code-bracket',        label: 'SQL'      },
]

// ── Resizable pane (middle width) ──────────────────────────────
const paneWidth = ref(280) // px
const isResizing = ref(false)

function startResize(e: MouseEvent) {
  isResizing.value = true
  const startX = e.clientX
  const startW = paneWidth.value

  const onMove = (ev: MouseEvent) => {
    const delta = ev.clientX - startX
    paneWidth.value = Math.max(200, Math.min(480, startW + delta))
  }
  const onUp = () => {
    isResizing.value = false
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseup', onUp)
  }
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', onUp)
}
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden" style="background: #060c1a; color: #e2e8f0;">

    <!-- ── Main workspace (top ~67%) ──────────────────────────── -->
    <div class="flex overflow-hidden flex-1" style="min-height: 0;">

      <!-- ── Icon sidebar (tab switcher) ─────────────────────── -->
      <nav
        class="w-14 flex flex-col items-center py-3 gap-1 shrink-0 border-r border-white/5"
        style="background: #060c1a;"
      >
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :title="tab.label"
          class="relative w-10 h-10 rounded-xl flex flex-col items-center justify-center gap-0.5 transition-all duration-150"
          :class="ws.activeTab === tab.id
            ? 'text-white'
            : 'text-slate-600 hover:text-slate-300 hover:bg-white/5'"
          :style="ws.activeTab === tab.id
            ? 'background: rgba(99,102,241,0.15); box-shadow: inset 0 0 0 1px rgba(99,102,241,0.3);'
            : ''"
          @click="ws.activeTab = tab.id"
        >
          <UIcon :name="tab.icon" class="size-4.5" />
          <span class="text-[8px] font-medium leading-none">{{ tab.label }}</span>

          <!-- Active indicator bar -->
          <div
            v-if="ws.activeTab === tab.id"
            class="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-r-full bg-indigo-400"
          />
        </button>

        <div class="flex-1" />

        <!-- Settings -->
        <button
          class="w-10 h-10 rounded-xl flex items-center justify-center text-slate-700 hover:text-slate-400 hover:bg-white/5 transition-all"
          title="Settings"
        >
          <UIcon name="i-heroicons-cog-6-tooth" class="size-4" />
        </button>
      </nav>

      <!-- ── Content pane (tab-dependent) ────────────────────── -->
      <div
        class="flex flex-col border-r border-white/5 overflow-hidden shrink-0"
        :style="`width: ${paneWidth}px; background: #080e1d;`"
      >
        <WorkspaceSidePane />
      </div>

      <!-- Resize handle -->
      <div
        class="w-1 shrink-0 cursor-col-resize hover:bg-indigo-500/40 transition-colors"
        :class="isResizing ? 'bg-indigo-500/60' : 'bg-transparent'"
        @mousedown="startResize"
      />

      <!-- ── ER Diagram canvas ─────────────────────────────────── -->
      <div class="flex-1 overflow-hidden min-w-0">
        <WorkspaceErCanvas />
      </div>
    </div>

    <!-- ── Query results (bottom ~33%) ─────────────────────────── -->
    <div
      class="flex flex-col border-t border-white/5 overflow-hidden"
      style="height: 33vh; background: #080e1d;"
    >
      <WorkspaceQueryPanel />
    </div>

  </div>
</template>
