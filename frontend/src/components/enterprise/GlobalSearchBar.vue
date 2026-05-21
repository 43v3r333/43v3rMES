<script setup lang="ts">
import { ref } from 'vue'
import { Search, Loader2 } from 'lucide-vue-next'

const query = ref('')
const isSearching = ref(false)
const results = ref<any[]>([])

const handleSearch = async () => {
  if (query.value.length < 2) return
  isSearching.value = true
  // Mock search call
  setTimeout(() => {
    isSearching.value = false
  }, 500)
}
</script>

<template>
  <div class="relative w-full max-w-md group">
    <div class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors">
      <Loader2 v-if="isSearching" class="h-4 w-4 animate-spin" />
      <Search v-else class="h-4 w-4" />
    </div>
    <input
      v-model="query"
      @input="handleSearch"
      type="text"
      placeholder="Global Operational Search (Alt+S)"
      class="w-full pl-9 pr-4 py-2 bg-muted/30 border border-transparent rounded-md text-xs font-bold uppercase tracking-tight focus:bg-background focus:border-primary outline-none transition-all"
    />
  </div>
</template>
