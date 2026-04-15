<template>
  <div class="h-screen flex flex-col overflow-hidden" style="background-color: #020617; color: #f1f5f9;">
    <AppWorkspaceNavbar />
    <main class="flex-1 overflow-hidden">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// Workspace layout: Navbar + content, no footer, full screen.
</script>
