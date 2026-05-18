<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold">Operational Dashboard</h1>
    <div class="grid grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="bg-white p-6 rounded shadow border">
        <div class="text-sm text-gray-500">KPI {{ i }}</div>
        <div class="text-2xl font-bold mt-2">99.9%</div>
      </div>
    </div>
  </div>
</template>
