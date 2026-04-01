<script setup lang="ts">
import Footer from "@/theme/components/Footer.vue";
import Widgets from "@/theme/sections/sales/Widgets.vue";
import RecentOrders from "@/theme/sections/sales/RecentOrders.vue";
import ProjectStatus from "@/theme/sections/sales/ProjectStatus.vue";
import EarningsReport from "@/theme/sections/sales/EarningsReport.vue";
import PopularProducts from "@/theme/sections/sales/PopularProducts.vue";
import LeadsVsCustomers from "@/theme/sections/sales/LeadsVsCustomers.vue";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <!-- Widget Cards -->
    <Widgets />

    <!-- Earnings Report Graph -->
    <EarningsReport />

    <!-- Lead and Customers Analytics Graph -->
    <LeadsVsCustomers />

    <!-- Project Status Graph -->
    <ProjectStatus />

    <!-- Popular Products Table List -->
    <PopularProducts />

    <!-- Recent Orders List -->
    <RecentOrders />

    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>
