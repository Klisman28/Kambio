<script setup lang="ts">
// SHADCN COMPONENTS
import { Card } from "@/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
// CUSTOM COMPOSABLE
import { useOrderHistories } from "./hooks/useOrderHistories";

const { orderHistories, isLoading } = useOrderHistories();
</script>

<template>
  <div class="col-span-full xl:col-span-6">
    <div class="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-2">
      <!-- SHOW LOADING SKELETONS -->
      <template v-if="isLoading">
        <Card class="p-6" v-for="item in 6" :key="item">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-md bg-skeleton animate-pulse"></div>

            <div class="flex-1 space-y-3">
              <p class="w-2/3 h-3 rounded-md bg-skeleton animate-pulse"></p>
              <p class="rounded-md h-7 w-28 bg-skeleton animate-pulse"></p>
            </div>
          </div>
        </Card>
      </template>

      <!-- SHOW DATA WHEN IS LOADED -->
      <template v-if="!isLoading && orderHistories.length">
        <Card v-for="item in orderHistories" class="p-6">
          <div class="flex items-center gap-4">
            <div
              class="grid rounded-md size-11 bg-slate-300/20 dark:bg-slate-600/20 place-items-center">
              <Icon :name="item.icon" :size="24" :strokeWidth="2" :class="item.color" />
            </div>

            <div>
              <p class="text-sm font-semibold">{{ item.title }}</p>
              <p class="text-2xl font-semibold" :class="item.color">
                {{ item.totalOrder }}
              </p>
            </div>
          </div>
        </Card>
      </template>
    </div>
  </div>
</template>
