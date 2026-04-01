<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// CUSTOM COMPONENTS
import Rating from "@/theme/components/Rating.vue";
// CUSTOM DATA
import { topSellingProducts } from "@/theme/data/dashboards/sass";
</script>

<template>
  <Card class="px-5 py-6 col-span-full xl:col-span-4">
    <CardTitle class="mb-6">Top Selling Products</CardTitle>

    <CardContent class="space-y-5">
      <div v-for="product in topSellingProducts" class="flex items-center gap-4">
        <Avatar shape="square" size="base">
          <AvatarImage :src="product.img" alt="product" />
          <AvatarFallback>{{ product.productName }}</AvatarFallback>
        </Avatar>

        <div class="space-y-1">
          <p class="text-sm font-semibold">
            {{ product.productName }}
          </p>

          <Rating :rating="product.rating" />

          <p class="pt-1 text-xs font-semibold">${{ product.price }}</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
