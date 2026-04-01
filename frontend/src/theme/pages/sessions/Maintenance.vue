<script setup lang="ts">
import { RouterLink } from "vue-router";
// SHADCN COMPONENTS
import Button from "@/theme/components/ui/button/Button.vue";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
</script>

<template>
  <div class="flex items-center justify-center h-screen text-center">
    <div class="p-30 xl:w-2/3">
      <img
        alt="maintenance"
        src="/images/illustration/maintenance-2.svg"
        class="w-64 mx-auto mb-10 sm:w-96 xl:mb-20" />

      <h2 class="mt-6 mb-2 text-2xl font-bold sm:text-4xl">We are under scheduled maintenance.</h2>
      <p class="text-sm sm:text-base text-muted">
        Sorry for the inconvenience, we will be back shortly!
      </p>

      <Button :as="RouterLink" to="/" variant="link" class="mt-8">
        <Icon name="ChevronLeft" :size="20" class="pe-1 rtl:rotate-180" :strokeWidth="2" />
        Go Back
      </Button>
    </div>
  </div>
</template>
