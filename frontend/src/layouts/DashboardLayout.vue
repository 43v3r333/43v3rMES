<script setup lang="ts">import { RouterView } from 'vue-router'</script>
<template>
  <div class="min-h-screen flex bg-gray-50">
    <aside class="w-64 bg-slate-900 text-white p-6">
      <h1 class="text-xl font-bold mb-8">AI MES</h1>
      <nav class="space-y-2">
        <router-link to="/" class="block p-2 hover:bg-slate-800 rounded">Dashboard</router-link>
      </nav>
    </aside>
    <main class="flex-1 p-8"><RouterView /></main>
  </div>
</template>
