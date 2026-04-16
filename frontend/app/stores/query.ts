import { defineStore } from 'pinia'
import { useConnectionStore } from './connection'
import type { TableMetadata, QueryAST } from '~/types'

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
    activeTableName: null as string | null,
    tableSearchQuery: '',
    columnSearchQuery: '',
    results: [] as any[],
    sql: '',
    isLoading: false,
    schemaError: null as string | null,
    queryError: null as string | null
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
      this.schemaError = null
      try {
        const config = useRuntimeConfig()
        const connectionStore = useConnectionStore()
        
        console.log(`Fetching schema from database: ${connectionStore.activeConnection}`)
        
        // Select internal URL for SSR, external for Client
        const apiBase = import.meta.server ? (config as any).apiBase : config.public.apiBase
        
        const response = await $fetch(`${apiBase}/api/schema`, {
          headers: {
            'X-Database-Alias': connectionStore.activeConnection
          }
        })
        console.log('Schema received:', response)
        
        const schema = response as { tables: TableMetadata[] }
        this.availableTables = schema.tables
        
        if (!this.query.from && schema.tables && schema.tables.length > 0) {
          this.query.from = schema.tables[0]!.name
        }
      } catch (e: any) {
        console.error('Schema fetch error:', e)
        this.schemaError = e.message || 'Failed to load schema'
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
      this.queryError = null
      
      try {
        const config = useRuntimeConfig()
        const connectionStore = useConnectionStore()
        
        console.log(`Executing query on database: ${connectionStore.activeConnection}`)
        
        const apiBase = import.meta.server ? (config as any).apiBase : config.public.apiBase
        
        const response = await $fetch(`${apiBase}/api/query/execute`, {
          method: 'POST',
          body: this.query,
          headers: {
            'X-Database-Alias': connectionStore.activeConnection
          }
        })
        console.log('Query response:', response)

        const res = response as any
        this.results = res.results
        this.sql = res.sql
      } catch (e: any) {
        console.error('Execution error:', e)
        this.queryError = e.message || 'Query execution failed'
        throw e
      } finally {
        this.isLoading = false
      }
    }
  }
})
