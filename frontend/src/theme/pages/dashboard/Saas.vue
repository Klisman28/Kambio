<script setup lang="ts">
import Footer from "@/theme/components/Footer.vue";
import Widgets from "@/theme/sections/saas/Widgets.vue";
import Analytics from "@/theme/sections/saas/Analytics.vue";
import TotalSpend from "@/theme/sections/saas/TotalSpend.vue";
import RecentOrders from "@/theme/sections/saas/RecentOrders.vue";
import TopSellingProducts from "@/theme/sections/saas/TopSellingProducts.vue";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <!-- Widget Cards -->
    <Widgets />

    <!-- Total Spend Graph -->
    <TotalSpend />

    <!-- Analytics Graph -->
    <Analytics />

    <!-- Recent Orders Table -->
    <RecentOrders />

    <!-- Top Selling Product List -->
    <TopSellingProducts />

    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>
