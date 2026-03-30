<template>
  <div
    v-for="i in 4"
    :key="i"
    class="pb-5 mb-5 space-y-2 border-b border-border last:border-b-0 last:mb-0 animate-pulse">
    <div class="flex items-center gap-3 mb-3">
      <div class="w-10 h-10 rounded-md bg-skeleton"></div>

      <div class="space-y-3">
        <div class="h-2 rounded-md w-60 bg-skeleton"></div>
        <div class="w-32 h-2 rounded-md bg-skeleton"></div>
      </div>
    </div>

    <div class="inline-flex gap-3">
      <div v-for="i in 5" :key="i" class="w-4 h-4 rounded-full bg-skeleton"></div>
    </div>

    <div class="h-2 rounded-md w-90 bg-skeleton"></div>

    <div class="flex items-start gap-5 pt-2">
      <div class="w-16 h-2 rounded-md bg-skeleton"></div>
      <div class="w-16 h-2 rounded-md bg-skeleton"></div>
    </div>
  </div>
</template>
