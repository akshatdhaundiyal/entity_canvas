import { defineStore } from 'pinia'

export interface ColumnMetadata {
  name: string
  data_type: string
  is_nullable: boolean
  default_value: string | null
}

export interface TableMetadata {
  name: string
  columns: ColumnMetadata[]
}

export interface QueryAST {
  select: { table: string; column: string; alias?: string }[]
  from: string
  joins: { table: string; on: string; type: 'INNER' | 'LEFT' }[]
  where: { column: string; operator: string; value: any; logic: 'AND' | 'OR' }[]
  sorts: { column: string; direction: 'ASC' | 'DESC' }[]
  limit: number
}

export const useQueryStore = defineStore('query', {
  state: () => ({
    query: {
      select: [],
      from: '',
      joins: [],
      where: [],
      sorts: [],
      limit: 100
    } as QueryAST,
    availableTables: [] as TableMetadata[],
    activeTableName: '' as string,
    tableSearchQuery: '',
    columnSearchQuery: '',
    results: [] as any[],
    sql: '',
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    filteredTables: (state) => {
      if (!state.tableSearchQuery) return state.availableTables
      const query = state.tableSearchQuery.toLowerCase()
      return state.availableTables.filter(t => t.name.toLowerCase().includes(query))
    },

    activeTable: (state) => {
      return state.availableTables.find(t => t.name === state.activeTableName) || null
    },

    filteredColumns: (state) => {
      const table = state.availableTables.find(t => t.name === state.activeTableName)
      if (!table) return []
      if (!state.columnSearchQuery) return table.columns
      
      const query = state.columnSearchQuery.toLowerCase()
      return table.columns.filter(c => c.name.toLowerCase().includes(query))
    }
  },

  actions: {
    async fetchSchema() {
      this.isLoading = true
      try {
        console.log('Fetching schema from backend...')
        const response = await $fetch('http://localhost:8000/api/schema')
        console.log('Schema received:', response)
        
        const schema = response as { tables: TableMetadata[] }
        this.availableTables = schema.tables
        
        if (!this.query.from && schema.tables && schema.tables.length > 0) {
          this.query.from = schema.tables[0]!.name
        }
      } catch (e: any) {
        console.error('Schema fetch error:', e)
        this.error = `Failed to fetch schema: ${e.message}`
      } finally {
        this.isLoading = false
      }
    },

    addColumn(table: string, column: string) {
      if (!this.query.select.find(c => c.table === table && c.column === column)) {
        this.query.select.push({ table, column })
      }
    },

    removeColumn(index: number) {
      this.query.select.splice(index, 1)
    },

    addFilter(column: string, operator: string = '=', value: any = '') {
      this.query.where.push({ column, operator, value, logic: 'AND' })
    },

    async executeQuery() {
      this.isLoading = true
      this.error = null
      
      try {
        console.log('Executing query:', this.query)
        const response = await $fetch('http://localhost:8000/api/query/execute', {
          method: 'POST',
          body: this.query
        })
        console.log('Query response:', response)

        const res = response as any
        this.results = res.results
        this.sql = res.sql
      } catch (e: any) {
        console.error('Execution error:', e)
        this.error = e.message
      } finally {
        this.isLoading = false
      }
    }
  }
})
