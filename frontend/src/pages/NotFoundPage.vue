<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-background p-4 text-center">
    <h1 class="text-6xl font-bold text-primary mb-4">404</h1>
    <h2 class="text-2xl font-semibold mb-2">Page Not Found</h2>
    <p class="text-muted-foreground mb-8">The industrial route you are looking for does not exist.</p>
    <router-link to="/" class="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:bg-primary/90 transition-colors">
      Back to Dashboard
    </router-link>
  </div>
</template>
