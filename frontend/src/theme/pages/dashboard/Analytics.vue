<script setup lang="ts">
import Footer from "@/theme/components/Footer.vue";
import UserDevice from "@/theme/sections/analytics/UserDevice.vue";
import WidgetList from "@/theme/sections/analytics/WidgetList.vue";
import LatestOrders from "@/theme/sections/analytics/LatestOrders.vue";
import ExpenseHistory from "@/theme/sections/analytics/ExpenseHistory.vue";
import UsersByContinent from "@/theme/sections/analytics/UsersByContinent.vue";
import DailyVisitInsights from "@/theme/sections/analytics/DailyVisitInsights.vue";
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
