import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useConnectionStore = defineStore('connection', () => {
  const activeConnection = ref<string>('Local')
  const availableConnections = ref<{ label: string, value: string }[]>([{ label: 'Local', value: 'Local' }])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const config = useRuntimeConfig()
  const apiBase = config.public.apiBaseUrl

  async function fetchConnections() {
    if (loading.value) return
    loading.value = true
    error.value = null
    console.log('DEBUG: fetchConnections starting for', `${apiBase}/api/connections`)
    try {
      // Use $fetch with a timestamp to bust any cache
      const data = await $fetch<{ connections: string[] }>(`${apiBase}/api/connections?t=${Date.now()}`)
      
      if (data && data.connections && data.connections.length > 0) {
        // Map strings to objects for better UI reactivity
        availableConnections.value = data.connections.map(c => ({ label: c, value: c }))
        
        // Restore from localStorage if available
        const saved = localStorage.getItem('active-db-connection')
        if (saved && availableConnections.value.some(c => c.value === saved)) {
          activeConnection.value = saved
        } else {
          // If current selection is invalid, use first available
          if (!availableConnections.value.some(c => c.value === activeConnection.value)) {
            activeConnection.value = availableConnections.value[0].value
          }
        }
      }
    }
 catch (e: any) {
      error.value = e.message || 'Failed to fetch connections'
      console.error('Error fetching connections:', e)
    } finally {
      loading.value = false
    }
  }

  // Auto-fetch on store creation if on client
  if (import.meta.client) {
    fetchConnections()
  }

  function setConnection(alias: string) {
    activeConnection.value = alias
    localStorage.setItem('active-db-connection', alias)
    // Trigger a window reload to refresh all data or handled by components
    window.location.reload()
  }

  return {
    activeConnection,
    availableConnections,
    loading,
    error,
    fetchConnections,
    setConnection
  }
})
