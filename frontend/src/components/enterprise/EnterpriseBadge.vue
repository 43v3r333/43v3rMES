<script setup lang="ts">
defineProps<{
  variant?: 'info' | 'success' | 'warning' | 'error' | 'neutral';
}>();
</script>

<template>
  <span
    :class="[
      'px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter border',
      variant === 'success' ? 'bg-green-100 text-green-700 border-green-200' : '',
      variant === 'warning' ? 'bg-amber-100 text-amber-700 border-amber-200' : '',
      variant === 'error' ? 'bg-red-100 text-red-700 border-red-200' : '',
      variant === 'info' ? 'bg-blue-100 text-blue-700 border-blue-200' : '',
      !variant || variant === 'neutral' ? 'bg-muted text-muted-foreground border-border' : ''
    ]"
  >
    <slot />
  </span>
</template>
