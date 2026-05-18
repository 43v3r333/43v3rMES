<script setup lang="ts">
defineProps<{
  columns: { key: string; label: string }[];
  data: any[];
}>();
</script>

<template>
  <div class="w-full overflow-hidden border rounded-lg bg-card">
    <table class="w-full text-left text-sm">
      <thead class="bg-muted/50 border-b">
        <tr>
          <th v-for="col in columns" :key="col.key" class="px-6 py-3 font-medium">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y">
        <tr v-for="(row, i) in data" :key="i" class="hover:bg-muted/30 transition-colors">
          <td v-for="col in columns" :key="col.key" class="px-6 py-4">
            <slot :name="`cell(${col.key})`" :row="row">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
