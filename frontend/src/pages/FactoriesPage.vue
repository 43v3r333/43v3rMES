<script setup lang="ts">
import { onMounted } from 'vue'
import { useFactoryStore } from '@/stores/factory'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plus, Factory as FactoryIcon } from 'lucide-vue-next'

const factoryStore = useFactoryStore()

const columns = [
  { key: 'name', label: 'Factory Name' },
  { key: 'description', label: 'Description' },
  { key: 'created_at', label: 'Created' },
]

onMounted(() => {
  factoryStore.fetchFactories()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Enterprise Hierarchy</h1>
        <p class="text-sm text-muted-foreground">Define and manage your physical manufacturing locations.</p>
      </div>
      <BaseButton variant="primary">
        <Plus class="mr-2 h-4 w-4" />
        Add Factory
      </BaseButton>
    </div>

    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="factory in factoryStore.factories" :key="factory.id" class="bg-card border rounded-lg overflow-hidden flex flex-col shadow-sm">
        <div class="p-5 border-b bg-muted/10">
          <div class="flex items-start justify-between">
            <div class="h-10 w-10 rounded bg-primary/10 flex items-center justify-center text-primary">
              <FactoryIcon class="h-6 w-6" />
            </div>
            <BaseButton variant="ghost" class="h-8 w-8 p-0">...</BaseButton>
          </div>
          <h3 class="mt-4 font-bold text-lg">{{ factory.name }}</h3>
          <p class="text-xs text-muted-foreground line-clamp-2 mt-1">{{ factory.description || 'No description provided.' }}</p>
        </div>
        <div class="p-4 bg-muted/5 flex justify-between items-center text-xs text-muted-foreground font-medium">
          <span>ID: {{ factory.id.split('-')[0] }}...</span>
          <span>Added: {{ new Date(factory.created_at).toLocaleDateString() }}</span>
        </div>
      </div>
    </div>

    <div v-if="factoryStore.factories.length === 0" class="border-2 border-dashed rounded-lg py-24 text-center">
      <FactoryIcon class="mx-auto h-12 w-12 text-muted-foreground/30" />
      <h3 class="mt-4 text-lg font-semibold">No factories found</h3>
      <p class="text-muted-foreground">Get started by defining your first manufacturing facility.</p>
      <BaseButton variant="outline" class="mt-6">Create Initial Factory</BaseButton>
    </div>
  </div>
</template>
