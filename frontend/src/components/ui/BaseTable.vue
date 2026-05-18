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
          <th v-for="col in columns" :key="col.key" class="px-6 py-3 font-semibold uppercase tracking-wider text-[11px] text-muted-foreground">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody class="divide-y">
        <tr v-for="(row, i) in data" :key="i" class="hover:bg-muted/30 transition-colors group">
          <td v-for="col in columns" :key="col.key" class="px-6 py-4 whitespace-nowrap">
            <slot :name="`cell(${col.key})`" :row="row">
              <span class="text-foreground/80 font-medium">{{ row[col.key] }}</span>
            </slot>
          </td>
        </tr>
        <tr v-if="data.length === 0">
          <td :colspan="columns.length" class="text-center">
            <slot name="empty"></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
