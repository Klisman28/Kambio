<script setup lang="ts">
import { RouterLink } from "vue-router";
// SHADCN COMPONENTS
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";

// ===========================
interface Props {
  route: string;
  icon: string;
  title: string;
  description: string;
}
// ===========================

defineProps<Props>();
</script>

<template>
  <RouterLink :to="route">
    <Card class="border-0 shadow-none cursor-pointer">
      <CardContent>
        <div class="flex items-center gap-3 group">
          <div class="p-2 rounded-md text-primary bg-primary-light">
            <Icon :name="icon" :size="20" />
          </div>
          <div>
            <p class="text-sm font-medium group-hover:text-primary">
              {{ title }}
            </p>
            <p class="text-xs font-normal text-muted">
              {{ description }}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  </RouterLink>
</template>
