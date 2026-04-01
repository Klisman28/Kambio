<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// CUSTOM UTILS METHOD
import { currency } from "@/theme/lib/currency";
// CUSTOM DATA
import { recentOrders } from "@/theme/data/dashboards/sales";
</script>

<template>
  <Card class="p-6 col-span-full lg:col-span-4">
    <CardTitle class="flex justify-between mb-5">
      <p>Recent Orders</p>
      <Button variant="link">View all</Button>
    </CardTitle>

    <CardContent class="space-y-5">
      <div :key="order.id" v-for="order in recentOrders" class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <Avatar shape="square">
            <AvatarImage :src="order.img" alt="product" />
            <AvatarFallback>P</AvatarFallback>
          </Avatar>

          <div>
            <p class="font-semibold">
              {{ order.productName }}
            </p>

            <p class="text-xs font-normal text-muted">{{ order.time }} mins ago</p>
          </div>
        </div>

        <p class="font-semibold">{{ currency(order.price) }}</p>
      </div>
    </CardContent>
  </Card>
</template>
