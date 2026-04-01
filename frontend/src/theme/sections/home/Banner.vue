<script setup lang="ts">
import { RouterLink } from "vue-router";
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
</script>

<template>
  <div class="container px-4 py-20 mx-auto space-y-6 text-center">
    <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight!">
      Transform your development <br />
      with Powerful <span class="text-primary">Vuejs</span> dashboard
    </h2>

    <p class="text-base lg:text-lg text-muted">
      Uko includes well-designed dashboards, applications, <br />
      and pages in both light and dark color schemes.
    </p>

    <div class="flex gap-4 justify-center py-8">
      <Button :as="RouterLink" to="/learning-management" size="lg">Live Preview</Button>
      <Button
        :as="'a'"
        size="lg"
        target="_blank"
        variant="outline"
        href="https://themeforest.net/item/uko-vuejs-admin-dashboard/54554727">
        Buy Now ($19)
      </Button>
    </div>
  </div>
</template>
