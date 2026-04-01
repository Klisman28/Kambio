<script setup lang="ts">
import OrderList from "@/theme/sections/orders/OrderList.vue";
import OrderFilters from "@/theme/sections/orders/OrderFilters.vue";
import OrderHistory from "@/theme/sections/orders/OrderHistory.vue";
import OrderAnalytics from "@/theme/sections/orders/OrderAnalytics.vue";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <div class="col-span-full xl:col-span-6">
      <OrderHistory />
    </div>

    <div class="col-span-full xl:col-span-6">
      <OrderAnalytics />
    </div>
  </div>

  <!-- User Table Filter Actions -->
  <OrderFilters />

  <!-- Order List -->
  <OrderList />
</template>
