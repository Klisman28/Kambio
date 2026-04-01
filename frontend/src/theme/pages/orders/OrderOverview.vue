<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
// CUSTOM COMPONENTS
import OrderInfo from "@/theme/sections/orders/order-info";
import OrderStatus from "@/theme/sections/orders/order-status";
import OrderSummery from "@/theme/sections/orders/order-summery";
import OrderWidgets from "@/theme/sections/orders/order-widgets";
import {
  OrderInfoSkeleton,
  OrderStatusSkeleton,
  OrderWidgetSkeleton,
  OrderSummerySkeleton
} from "@/theme/sections/orders/skeletons";
// TYPES
import { Order } from "@/theme/types/Order";

const route = useRoute();
const router = useRouter();

const error = ref("");
const isLoading = ref(true);
const order = ref<Order>();

const getOrder = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Order>("/api/orders", {
      params: { id: +route.params.id }
    });

    if (data) order.value = data;
    else router.push({ name: "NotFound" });
  } catch (err) {
    error.value = "Something went wrong";
  } finally {
    isLoading.value = false;
  }
};

onMounted(getOrder);
</script>

<template>
  <!-- SHOW LOADING SKELETON -->
  <template v-if="isLoading">
    <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
      <OrderInfoSkeleton />
    </div>

    <div class="grid grid-cols-12 mb-6 gap-7">
      <OrderWidgetSkeleton />
    </div>

    <div class="grid items-start grid-cols-1 mb-6 gap-7 xl:grid-cols-2">
      <OrderSummerySkeleton />
      <OrderStatusSkeleton />
    </div>
  </template>

  <!-- SHOW PAGE WHEN DATA IS LOADED -->
  <template v-if="!isLoading && order">
    <OrderInfo :order="order" />
    <OrderWidgets :order="order" />

    <div class="grid items-start grid-cols-1 mb-6 gap-7 xl:grid-cols-2">
      <OrderSummery :order="order" />
      <OrderStatus :order="order" />
    </div>
  </template>
</template>
