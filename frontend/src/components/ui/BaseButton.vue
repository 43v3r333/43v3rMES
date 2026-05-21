<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  loading?: boolean;
}>();
</script>

<template>
  <button
    class="inline-flex items-center justify-center px-4 py-2 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none"
    :class="[
      variant === 'primary' ? 'bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-primary' : '',
      variant === 'secondary' ? 'bg-secondary text-secondary-foreground hover:bg-secondary/80 focus:ring-secondary' : '',
      variant === 'outline' ? 'border border-input hover:bg-accent hover:text-accent-foreground' : '',
      variant === 'destructive' ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90 focus:ring-destructive' : '',
      !variant ? 'bg-primary text-primary-foreground hover:bg-primary/90' : ''
    ]"
    :disabled="loading"
  >
    <span v-if="loading" class="mr-2 h-4 w-4 animate-spin border-2 border-current border-t-transparent rounded-full"></span>
    <slot />
  </button>
</template>
