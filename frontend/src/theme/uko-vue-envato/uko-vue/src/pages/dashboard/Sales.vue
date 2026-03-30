<script setup lang="ts">
import Footer from "@/components/Footer.vue";
import Widgets from "@/sections/sales/Widgets.vue";
import RecentOrders from "@/sections/sales/RecentOrders.vue";
import ProjectStatus from "@/sections/sales/ProjectStatus.vue";
import EarningsReport from "@/sections/sales/EarningsReport.vue";
import PopularProducts from "@/sections/sales/PopularProducts.vue";
import LeadsVsCustomers from "@/sections/sales/LeadsVsCustomers.vue";
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
