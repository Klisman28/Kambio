<script setup lang="ts">
// SHADCN COMPONENTS
import { Badge } from "@/theme/components/ui/badge";
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// CUSTOM DATA
import { widgets } from "@/theme/data/dashboards/analytics";
</script>

<template>
  <Card class="p-6 col-span-full xl:col-span-3 md:col-span-6" v-for="widget in widgets">
    <CardContent>
      <p class="font-medium text-muted">
        {{ widget.title }}
      </p>

      <div class="flex items-center gap-2 pt-2 pb-1">
        <p class="text-2xl font-bold">
          {{ widget.number }}
        </p>

        <Badge :variant="widget.isIncrease ? 'default' : 'destructive'" class="text-xs font-medium">
          {{ widget.percentage }}%
        </Badge>
      </div>

      <div class="flex items-center gap-2">
        <Icon name="Eye" :size="16" :strokeWidth="2" class="text-muted" />
        <p class="text-xs font-medium text-muted">Last week {{ widget.weeklyViews }}</p>
      </div>
    </CardContent>
  </Card>
</template>
