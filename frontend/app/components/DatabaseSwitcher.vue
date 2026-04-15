<template>
  <div class="flex items-center gap-1.5 p-1 rounded-full border border-white/5 bg-white/3">
    <UButton
      v-for="conn in store.availableConnections"
      :key="conn.value"
      size="xs"
      :variant="store.activeConnection === conn.value ? 'solid' : 'ghost'"
      :color="store.activeConnection === conn.value ? 'primary' : 'neutral'"
      class="rounded-full px-3 transition-all duration-200"
      @click="onSwitch(conn.value)"
    >
      <span class="text-[10px] font-bold uppercase tracking-wider">{{ conn.label }}</span>
    </UButton>
  </div>
</template>

<script setup lang="ts">
import { useConnectionStore } from '~/stores/connection'

const store = useConnectionStore()

const onSwitch = (val: string) => {
  store.setConnection(val)
}
</script>

<style scoped>
/* Optional: additive styling for premium feel */
:deep(.u-select-menu-button) {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #e2e8f0 !important;
  border-radius: 9999px !important;
  transition: all 0.2s ease;
}

:deep(.u-select-menu-button:hover) {
  background: rgba(255, 255, 255, 0.07) !important;
  border-color: rgba(99, 102, 241, 0.5) !important;
}
</style>
