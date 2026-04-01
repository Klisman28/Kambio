<script setup lang="ts">
// CUSTOM COMPONENTS
import OrderInfoCard from "./OrderInfoCard.vue";
// TYPES
import { Order } from "@/theme/types/Order";

defineProps<{ order: Order }>();
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <OrderInfoCard
      icon="Truck"
      iconColor="success"
      :title="order.customer.name"
      heading="Shipping Details">
      {{ order.shipping }}
    </OrderInfoCard>

    <OrderInfoCard
      icon="CreditCard"
      iconColor="default"
      :title="order.customer.name"
      heading="Billing Details">
      {{ order.billing }}
    </OrderInfoCard>

    <OrderInfoCard
      icon="DollarSign"
      iconColor="warning"
      title="ID: #TSD456DF41SD5"
      heading="Payment Details">
      Payment Method: {{ order.payment.paymentMethod }} <br />
      Number: {{ order.payment.cardNumber }}
    </OrderInfoCard>

    <OrderInfoCard
      icon="Book"
      iconColor="destructive"
      title="Marie Prohaska"
      heading="Customer Info">
      {{ order.customer.email }} <br />
      {{ order.customer.phone }}
    </OrderInfoCard>
  </div>
</template>
