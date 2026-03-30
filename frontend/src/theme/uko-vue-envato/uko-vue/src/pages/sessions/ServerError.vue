<script setup lang="ts">
import { RouterLink } from "vue-router";
// SHADCN COMPONENTS
import Button from "@/components/ui/button/Button.vue";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
</script>

<template>
  <div class="flex items-center justify-center h-screen text-center">
    <div class="p-30 xl:w-1/3">
      <img
        src="/images/illustration/500.svg"
        alt="maintenance"
        class="w-56 mx-auto mb-10 sm:w-96 xl:mb-20" />

      <h2 class="mt-6 mb-2 text-2xl font-bold sm:text-4xl">Something went wrong!</h2>
      <p class="text-sm sm:text-base text-muted">
        Server Error 500. Our staff has been notified, <br />
        thank you for your understanding.
      </p>

      <Button :as="RouterLink" to="/" variant="link" class="mt-8">
        <Icon name="ChevronLeft" :size="20" class="pe-1 rtl:rotate-180" :strokeWidth="2" />
        Go Back
      </Button>
    </div>
  </div>
</template>
