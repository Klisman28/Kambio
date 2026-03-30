<script setup lang="ts">
import Footer from "@/components/Footer.vue";
import UserDevice from "@/sections/analytics/UserDevice.vue";
import WidgetList from "@/sections/analytics/WidgetList.vue";
import LatestOrders from "@/sections/analytics/LatestOrders.vue";
import ExpenseHistory from "@/sections/analytics/ExpenseHistory.vue";
import UsersByContinent from "@/sections/analytics/UsersByContinent.vue";
import DailyVisitInsights from "@/sections/analytics/DailyVisitInsights.vue";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <!-- Widget List Cards -->
    <WidgetList />

    <!-- Expense History Graph -->
    <ExpenseHistory />

    <!-- User Device List -->
    <UserDevice />

    <!-- Latest Orders Table List -->
    <LatestOrders />

    <!-- Daily Visit Insights Graph -->
    <DailyVisitInsights />

    <!-- Users By Continents List -->
    <UsersByContinent />

    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>
