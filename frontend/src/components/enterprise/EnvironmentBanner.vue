<script setup lang="ts">
import { Terminal, ShieldAlert } from 'lucide-vue-next'
</script>

<template>
  <div class="bg-amber-500 text-amber-950 px-4 py-1.5 flex items-center justify-between text-[10px] font-black uppercase tracking-widest shadow-inner">
    <div class="flex items-center space-x-3">
      <span class="flex items-center bg-amber-600/20 px-2 py-0.5 rounded">
        <Terminal class="h-3 w-3 mr-2" />
        Developer Node: 43v3r-DEV-01
      </span>
      <span>Enterprise Testing Mode Enabled</span>
    </div>
    <div class="flex items-center space-x-4">
      <span class="flex items-center text-amber-900/60">
        <ShieldAlert class="h-3 w-3 mr-1" />
        Simulation Active
      </span>
      <button class="bg-amber-900 text-amber-50 px-2 py-0.5 rounded hover:bg-amber-950 transition-colors">
        System Diagnostics
      </button>
    </div>
  </div>
</template>
