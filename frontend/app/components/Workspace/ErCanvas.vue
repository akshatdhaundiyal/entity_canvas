<!-- SVG-based ER diagram canvas with pan/zoom -->
<script setup lang="ts">
import { useQueryStore } from '~/stores/query'
import { useWorkspaceStore } from '~/stores/workspace'

const query = useQueryStore()
const ws = useWorkspaceStore()

// ── Layout constants ────────────────────────────────────────────
const TW = 210         // table width
const HEADER_H = 40   // table header height
const ROW_H = 28       // column row height

// ── Table positions (x, y) ──────────────────────────────────────
// Computed layout: arrange into columns automatically
const TABLE_POSITIONS: Record<string, { x: number; y: number }> = {
  // Defaults for unknown tables — auto-grid below
}

const VIEWBOX_W = 1160
const VIEWBOX_H = 560

const tableLayout = computed(() => {
  const tables = query.availableTables
  if (tables.length === 0) return []

  // Use preset positions if table name matches common patterns,
  // otherwise arrange in a grid (max 3 per column)
  const layout: { name: string; x: number; y: number; h: number }[] = []
  const PADDING_X = 40
  const PADDING_Y = 50
  const GAP_X = 60
  const GAP_Y = 40
  const COLS = 3

  tables.forEach((t, i) => {
    const col = i % COLS
    const row = Math.floor(i / COLS)

    // Height of this box
    const h = HEADER_H + t.columns.length * ROW_H

    // For two-col layouts, stagger columns nicely
    let x = PADDING_X + col * (TW + GAP_X)
    let y = PADDING_Y + row * (200 + GAP_Y)

    // Use manual overrides for top 5 tables if present
    const manualPos = TABLE_POSITIONS[t.name]
    if (manualPos) {
      x = manualPos.x
      y = manualPos.y
    }

    layout.push({ name: t.name, x, y, h })
  })

  return layout
})

function tableH(tableName: string) {
  const t = query.availableTables.find(t => t.name === tableName)
  if (!t) return HEADER_H
  return HEADER_H + t.columns.length * ROW_H
}

function colRowY(tableName: string, colName: string) {
  const t = query.availableTables.find(t => t.name === tableName)
  if (!t) return 0
  const idx = t.columns.findIndex(c => c.name === colName)
  const pos = tableLayout.value.find(p => p.name === tableName)
  if (!pos) return 0
  return pos.y + HEADER_H + idx * ROW_H + ROW_H / 2
}

function tableX(tableName: string) {
  return tableLayout.value.find(p => p.name === tableName)?.x ?? 0
}
function tableY(tableName: string) {
  return tableLayout.value.find(p => p.name === tableName)?.y ?? 0
}

// ── Relation paths ───────────────────────────────────────────────
const relationPaths = computed(() =>
  ws.detectedRelations.map(edge => {
    // FK side (fromTable.fromCol) — "many" end
    const fromX = tableX(edge.fromTable)
    const fromY = colRowY(edge.fromTable, edge.fromCol)
    const fromRight = fromX + TW

    // PK side (toTable.toCol) — "one" end
    const toX = tableX(edge.toTable)
    const toY = colRowY(edge.toTable, edge.toCol)
    const toRight = toX + TW

    // Determine if FK is to the right or left of PK table
    let startX: number, endX: number, startY: number, endY: number, c1x: number, c2x: number

    if (fromX > toX) {
      // FK table is to the right → connect left of FK to right of PK
      startX = fromX
      endX = toRight
      startY = fromY
      endY = toY
      c1x = fromX - (fromX - toRight) / 2
      c2x = fromX - (fromX - toRight) / 2
    } else {
      // FK table is to the left → connect right of FK to left of PK
      startX = fromRight
      endX = toX
      startY = fromY
      endY = toY
      c1x = fromRight + (toX - fromRight) / 2
      c2x = fromRight + (toX - fromRight) / 2
    }

    const path = `M${startX},${startY} C${c1x},${startY} ${c2x},${endY} ${endX},${endY}`
    const color = ws.tableColor(edge.fromTable)
    return { path, color, edge }
  })
)

// ── Pan / Zoom ───────────────────────────────────────────────────
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const lastMouse = ref({ x: 0, y: 0 })

function onWheel(e: WheelEvent) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.08 : 0.08
  scale.value = Math.min(2.5, Math.max(0.3, scale.value + delta))
}

function onMouseDown(e: MouseEvent) {
  isPanning.value = true
  lastMouse.value = { x: e.clientX, y: e.clientY }
}

function onMouseMove(e: MouseEvent) {
  if (!isPanning.value) return
  panX.value += e.clientX - lastMouse.value.x
  panY.value += e.clientY - lastMouse.value.y
  lastMouse.value = { x: e.clientX, y: e.clientY }
}

function onMouseUp() { isPanning.value = false }

function resetView() {
  scale.value = 1
  panX.value = 0
  panY.value = 0
}
</script>

<template>
  <div
    class="relative w-full h-full overflow-hidden select-none"
    style="background: #060c1a; cursor: grab;"
    :style="isPanning ? 'cursor: grabbing;' : ''"
    @wheel.passive="onWheel"
    @mousedown="onMouseDown"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
  >
    <!-- Empty state -->
    <div
      v-if="query.availableTables.length === 0 && !query.isLoading"
      class="absolute inset-0 flex flex-col items-center justify-center gap-4 text-slate-600 pointer-events-none"
    >
      <UIcon name="i-heroicons-circle-stack" class="size-12 opacity-30" />
      <p class="text-sm">No schema loaded</p>
    </div>

    <!-- Pan / zoom controls -->
    <div class="absolute top-3 right-3 z-10 flex flex-col gap-1">
      <button
        class="h-7 w-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/8 transition-colors"
        style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);"
        title="Zoom in"
        @click="scale = Math.min(2.5, scale + 0.15)"
      >
        <UIcon name="i-heroicons-plus" class="size-3.5" />
      </button>
      <button
        class="h-7 w-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/8 transition-colors"
        style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);"
        title="Zoom out"
        @click="scale = Math.max(0.3, scale - 0.15)"
      >
        <UIcon name="i-heroicons-minus" class="size-3.5" />
      </button>
      <button
        class="h-7 w-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/8 transition-colors"
        style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);"
        title="Reset view"
        @click="resetView"
      >
        <UIcon name="i-heroicons-arrows-pointing-in" class="size-3.5" />
      </button>
    </div>

    <!-- Scale badge -->
    <div class="absolute bottom-3 right-3 text-[10px] text-slate-600 tabular-nums">
      {{ Math.round(scale * 100) }}%
    </div>

    <!-- SVG canvas -->
    <svg
      :viewBox="`0 0 ${VIEWBOX_W} ${VIEWBOX_H}`"
      :width="VIEWBOX_W"
      :height="VIEWBOX_H"
      class="absolute top-0 left-0"
      :style="`transform: translate(${panX}px, ${panY}px) scale(${scale}); transform-origin: center center;`"
    >
      <defs>
        <!-- Arrow marker for FK end -->
        <marker
          v-for="edge in ws.detectedRelations"
          :id="`arrow-${edge.fromTable}-${edge.fromCol}`"
          :key="`marker-${edge.fromTable}-${edge.fromCol}`"
          markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"
        >
          <path d="M0,0 L0,6 L8,3 z" :fill="ws.tableColor(edge.fromTable)" opacity="0.7" />
        </marker>
        <!-- Dot marker for PK end -->
        <marker
          v-for="edge in ws.detectedRelations"
          :id="`dot-${edge.fromTable}-${edge.fromCol}`"
          :key="`dot-marker-${edge.fromTable}-${edge.fromCol}`"
          markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"
        >
          <circle cx="3" cy="3" r="2.5" :fill="ws.tableColor(edge.fromTable)" opacity="0.6" />
        </marker>
      </defs>

      <!-- ── Relation lines ──────────────────────────────────────── -->
      <path
        v-for="rel in relationPaths"
        :key="`${rel.edge.fromTable}-${rel.edge.fromCol}`"
        :d="rel.path"
        fill="none"
        :stroke="rel.color"
        :stroke-width="(ws.hoveredColumn === `${rel.edge.fromTable}.${rel.edge.fromCol}` || ws.hoveredTable === rel.edge.fromTable || ws.hoveredTable === rel.edge.toTable) ? 2.5 : 1.5"
        :stroke-opacity="(ws.hoveredColumn === `${rel.edge.fromTable}.${rel.edge.fromCol}` || ws.hoveredTable === rel.edge.fromTable || ws.hoveredTable === rel.edge.toTable) ? 1 : 0.45"
        :stroke-dasharray="(ws.hoveredColumn === `${rel.edge.fromTable}.${rel.edge.fromCol}` || ws.hoveredTable === rel.edge.fromTable || ws.hoveredTable === rel.edge.toTable) ? '0' : '5 3'"
        :marker-end="`url(#arrow-${rel.edge.fromTable}-${rel.edge.fromCol})`"
        :marker-start="`url(#dot-${rel.edge.fromTable}-${rel.edge.fromCol})`"
        class="er-line transition-all duration-300 pointer-events-none"
      />

      <!-- ── Table boxes ─────────────────────────────────────────── -->
      <g
        v-for="pos in tableLayout"
        :key="pos.name"
        :transform="`translate(${pos.x}, ${pos.y})`"
        class="er-table cursor-pointer group"
        @mouseenter="ws.hoveredTable = pos.name"
        @mouseleave="ws.resetHover()"
      >
        <!-- Shadow -->
        <rect
          :width="TW" :height="pos.h"
          rx="10" ry="10"
          fill="none"
          :filter="`drop-shadow(0 8px 32px ${ws.tableColor(pos.name)}${ws.hoveredTable === pos.name ? '60' : '20'})`"
          class="transition-all duration-300"
        />

        <!-- Outer border -->
        <rect
          :width="TW" :height="pos.h"
          rx="10" ry="10"
          fill="#0b1022"
          :stroke="ws.isTableSelected(pos.name) ? ws.tableColor(pos.name) : (ws.hoveredTable === pos.name ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.08)')"
          :stroke-width="ws.isTableSelected(pos.name) || ws.hoveredTable === pos.name ? 1.5 : 1"
          class="transition-all duration-200"
        />

        <!-- Header -->
        <g @click.stop="ws.toggleTable(pos.name)">
          <rect
            :width="TW" :height="HEADER_H"
            rx="10" ry="10"
            :fill="ws.tableColor(pos.name)"
            :opacity="ws.isTableSelected(pos.name) ? 0.95 : 0.6"
            class="transition-opacity duration-200"
          />
          <!-- Header bottom square corners overlay -->
          <rect
            :y="HEADER_H - 10" :width="TW" height="10"
            :fill="ws.tableColor(pos.name)"
            :opacity="ws.isTableSelected(pos.name) ? 0.95 : 0.6"
            class="transition-opacity duration-200"
          />

          <!-- Table name -->
          <text
            :x="TW / 2" :y="HEADER_H / 2 + 5"
            text-anchor="middle"
            font-size="12" font-weight="700" font-family="Inter, sans-serif"
            fill="white"
          >{{ pos.name }}</text>
        </g>

        <!-- Column rows -->
        <g 
          v-for="(col, ci) in query.availableTables.find(t => t.name === pos.name)?.columns ?? []" 
          :key="col.name"
          class="cursor-pointer"
          @mouseenter.stop="ws.hoveredColumn = `${pos.name}.${col.name}`"
          @mouseleave.stop="ws.hoveredColumn = null"
          @click.stop="ws.toggleColumn(`${pos.name}.${col.name}`)"
        >
          <!-- Row background (alternating + hover) -->
          <rect
            :y="HEADER_H + ci * ROW_H" :width="TW" :height="ROW_H"
            :fill="ws.hoveredColumn === `${pos.name}.${col.name}` ? 'rgba(255,255,255,0.06)' : (ci % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.1)')"
            :rx="ci === (query.availableTables.find(t => t.name === pos.name)?.columns.length ?? 0) - 1 ? 6 : 0"
            class="transition-colors duration-150"
          />

          <!-- PK icon -->
          <text
            v-if="col.name === 'id' || col.name.endsWith('_id')"
            x="10"
            :y="HEADER_H + ci * ROW_H + ROW_H / 2 + 4"
            font-size="8" font-family="monospace"
            :fill="col.name === 'id' ? '#fbbf24' : '#818cf8'"
            :opacity="ws.hoveredColumn === `${pos.name}.${col.name}` ? 1 : 0.6"
          >{{ col.name === 'id' ? 'PK' : 'FK' }}</text>

          <!-- Column name -->
          <text
            :x="col.name === 'id' || col.name.endsWith('_id') ? 30 : 12"
            :y="HEADER_H + ci * ROW_H + ROW_H / 2 + 4"
            font-size="11" font-family="'JetBrains Mono', monospace"
            :fill="ws.isColumnSelected(`${pos.name}.${col.name}`) ? '#e2e8f0' : (ws.hoveredColumn === `${pos.name}.${col.name}` ? '#94a3b8' : '#64748b')"
            :font-weight="ws.isColumnSelected(`${pos.name}.${col.name}`) ? '600' : '400'"
            class="transition-colors duration-150"
          >{{ col.name }}</text>

          <!-- Data type (right-aligned) -->
          <text
            :x="TW - 8"
            :y="HEADER_H + ci * ROW_H + ROW_H / 2 + 4"
            text-anchor="end"
            font-size="9" font-family="monospace"
            :fill="ws.hoveredColumn === `${pos.name}.${col.name}` ? 'rgba(148,163,184,0.8)' : 'rgba(100,116,139,0.4)'"
          >{{ col.data_type }}</text>

          <!-- Selected indicator dot -->
          <circle
            v-if="ws.isColumnSelected(`${pos.name}.${col.name}`)"
            :cx="TW - 6"
            :cy="HEADER_H + ci * ROW_H + ROW_H / 2"
            r="3"
            :fill="ws.tableColor(pos.name)"
            opacity="0.9"
          />
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.er-line {
  transition: stroke-opacity 0.2s;
}
.er-line:hover {
  stroke-opacity: 0.9;
}
.er-table {
  transition: filter 0.2s;
}
</style>
