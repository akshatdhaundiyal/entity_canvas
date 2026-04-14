import { defineStore } from 'pinia'
import { useQueryStore } from './query'

export type WorkspaceTab = 'tables' | 'cascaded' | 'selected' | 'filters' | 'sql'

/** Extended table metadata with UI color and FK relations */
export interface RelationEdge {
  fromTable: string
  fromCol: string
  toTable: string
  toCol: string
}

// Colour palette for tables (cycles if more than 8 tables)
const TABLE_COLORS = [
  '#6366f1', // indigo
  '#10b981', // emerald
  '#f59e0b', // amber
  '#0ea5e9', // sky
  '#a855f7', // purple
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f97316', // orange
]

export const useWorkspaceStore = defineStore('workspace', () => {
  const queryStore = useQueryStore()

  // ── UI state ────────────────────────────────────────────────────
  const activeTab = ref<WorkspaceTab>('tables')
  const selectedTableNames = ref<string[]>([])
  const selectedColumns = ref<string[]>([]) // 'table.column' format
  const hoveredTable = ref<string | null>(null)
  const hoveredColumn = ref<string | null>(null) // 'table.column' format

  const filters = ref<{ column: string; operator: string; value: any; logic: 'AND' | 'OR' }[]>([])
  const sorts = ref<{ column: string; direction: 'ASC' | 'DESC' }[]>([])
  const limit = ref(100)

  // ── Derived helpers ─────────────────────────────────────────────
  const tableColor = (name: string) => {
    const idx = queryStore.availableTables.findIndex(t => t.name === name)
    return TABLE_COLORS[idx % TABLE_COLORS.length] ?? '#6366f1'
  }

  /** True when any tables include names that look like FK columns (detect by _id suffix) */
  const detectedRelations = computed<RelationEdge[]>(() => {
    const edges: RelationEdge[] = []
    for (const table of queryStore.availableTables) {
      for (const col of table.columns) {
        if (col.name.endsWith('_id') && col.name !== 'id') {
          const refTableName = col.name.replace(/_id$/, '')
          // Try plural match  (user_id → users)
          const singular = refTableName
          const plural = refTableName + 's'
          const refTable = queryStore.availableTables.find(
            t => t.name === singular || t.name === plural
          )
          if (refTable) {
            edges.push({
              fromTable: table.name,
              fromCol: col.name,
              toTable: refTable.name,
              toCol: 'id',
            })
          }
        }
      }
    }
    return edges
  })

  /** Columns from selected tables + FK-cascaded columns from referenced tables */
  const cascadedColumns = computed(() => {
    const result: { table: string; col: string; type: string; cascaded: boolean }[] = []
    const visited = new Set<string>()

    for (const tName of selectedTableNames.value) {
      const table = queryStore.availableTables.find(t => t.name === tName)
      if (!table) continue

      for (const col of table.columns) {
        result.push({ table: tName, col: col.name, type: col.data_type, cascaded: false })
      }
      visited.add(tName)

      // Cascade FK refs
      for (const edge of detectedRelations.value) {
        if (edge.fromTable === tName && !visited.has(edge.toTable)) {
          const refTable = queryStore.availableTables.find(t => t.name === edge.toTable)
          if (refTable) {
            for (const col of refTable.columns) {
              result.push({ table: refTable.name, col: col.name, type: col.data_type, cascaded: true })
            }
            visited.add(edge.toTable)
          }
        }
      }
    }

    return result
  })

  /** Only the user-chosen columns (table.col format) */
  const chosenColumns = computed(() =>
    selectedColumns.value.map(tc => {
      const [table, col] = tc.split('.')
      return { table, col }
    })
  )

  /** Generated SQL from selected columns + detected joins */
  const generatedSQL = computed<string>(() => {
    const tablesInQuery = [...new Set(selectedColumns.value.map(c => c.split('.')[0] ?? ''))]
    if (tablesInQuery.length === 0)
      return '-- Select columns to generate SQL'

    const baseTable = tablesInQuery[0] as string

    const selectLines = selectedColumns.value.map(c => {
      const [t, col] = c.split('.')
      return `  ${t}.${col}`
    })

    const joins: string[] = []
    for (const t of tablesInQuery.slice(1)) {
      // Find edge linking baseTable ↔ t
      const edge = detectedRelations.value.find(
        e =>
          (e.fromTable === t && e.toTable === baseTable) ||
          (e.fromTable === baseTable && e.toTable === t)
      )
      if (edge) {
        if (edge.fromTable === t) {
          joins.push(`JOIN ${t} ON ${t}.${edge.fromCol} = ${baseTable}.${edge.toCol}`)
        } else {
          joins.push(`JOIN ${t} ON ${baseTable}.${edge.fromCol} = ${t}.${edge.toCol}`)
        }
      } else {
        joins.push(`JOIN ${t} ON ${t}.id = ${baseTable}.${t}_id`)
      }
    }

    const sqlLines = [
      'SELECT',
      selectLines.join(',\n'),
      `FROM ${baseTable}`,
    ]

    if (joins.length > 0) sqlLines.push(...joins)

    // Filters
    if (filters.value.length > 0) {
      const filterLines = filters.value.map((f, i) => {
        const prefix = i === 0 ? 'WHERE' : f.logic
        const val = typeof f.value === 'string' ? `'${f.value}'` : f.value
        return `${prefix} ${f.column} ${f.operator} ${val}`
      })
      sqlLines.push(...filterLines)
    }

    // Sorting
    if (sorts.value.length > 0) {
      const sortLines = sorts.value.map(s => `${s.column} ${s.direction}`)
      sqlLines.push(`ORDER BY ${sortLines.join(', ')}`)
    }

    // Limit
    if (limit.value !== null) {
      sqlLines.push(`LIMIT ${limit.value};`)
    } else {
      sqlLines[sqlLines.length - 1] += ';'
    }

    return sqlLines.join('\n')
  })

  // ── Actions ──────────────────────────────────────────────────────
  function toggleTable(name: string) {
    const idx = selectedTableNames.value.indexOf(name)
    if (idx === -1) {
      selectedTableNames.value.push(name)
    } else {
      selectedTableNames.value.splice(idx, 1)
      // Deselect columns from this table
      selectedColumns.value = selectedColumns.value.filter(c => !c.startsWith(name + '.'))
    }
  }

  function toggleColumn(tableCol: string) {
    const idx = selectedColumns.value.indexOf(tableCol)
    if (idx === -1) selectedColumns.value.push(tableCol)
    else selectedColumns.value.splice(idx, 1)
  }

  function isTableSelected(name: string) {
    return selectedTableNames.value.includes(name)
  }

  function isColumnSelected(tableCol: string) {
    return selectedColumns.value.includes(tableCol)
  }

  function moveColumn(from: number, to: number) {
    const arr = [...selectedColumns.value]
    const [item] = arr.splice(from, 1)
    arr.splice(to, 0, item!)
    selectedColumns.value = arr
  }

  function resetHover() {
    hoveredTable.value = null
    hoveredColumn.value = null
  }

  function addFilter(col: string) {
    filters.value.push({ column: col, operator: '=', value: '', logic: 'AND' })
    activeTab.value = 'filters'
  }

  function removeFilter(index: number) {
    filters.value.splice(index, 1)
  }

  function toggleSort(col: string) {
    const existing = sorts.value.find(s => s.column === col)
    if (!existing) {
      sorts.value.push({ column: col, direction: 'ASC' })
    } else if (existing.direction === 'ASC') {
      existing.direction = 'DESC'
    } else {
      const idx = sorts.value.findIndex(s => s.column === col)
      sorts.value.splice(idx, 1)
    }
  }

  return {
    activeTab,
    selectedTableNames,
    selectedColumns,
    hoveredTable,
    hoveredColumn,
    filters,
    sorts,
    limit,
    tableColor,
    detectedRelations,
    cascadedColumns,
    chosenColumns,
    generatedSQL,
    toggleTable,
    toggleColumn,
    isTableSelected,
    isColumnSelected,
    moveColumn,
    resetHover,
    addFilter,
    removeFilter,
    toggleSort,
  }
})
