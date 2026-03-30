<script setup lang="ts">
import axios from "axios";
import { push } from "notivue";
// SHADCN COMPONENTS
import {
  Select,
  SelectItem,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/components/ui/select";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENT
import TimelineItem from "./TimelineItem.vue";
import { OrderStatusSkeleton } from "../skeletons";
// CUSTOM COMPOSABLE
import { useOrderStatuses } from "../hooks/useOrderStatuses";
// TYPES
import { Order } from "@/types/Order";

const props = defineProps<{ order: Order }>();

const { statuses, isLoading } = useOrderStatuses();

const handleUpdateStatus = async (status: string) => {
  try {
    await axios.patch("/api/orders", { status }, { params: { id: props.order.id } });
    push.success("Status updated successfully");
  } catch (error) {
    push.error("Something went wrong");
  }
};
</script>

<template>
  <OrderStatusSkeleton v-if="isLoading" />

  <Card class="px-5 pt-5" v-if="!isLoading && statuses.length">
    <div class="flex items-start justify-between mb-8">
      <CardTitle class="text-base">Order Status</CardTitle>

      <Select
        @update:modelValue="handleUpdateStatus"
        :defaultValue="order.status.toLowerCase()"
        :disabled="order.status === 'Delivered'">
        <SelectTrigger
          class="text-[13px] font-semibold w-20 p-0 border-none rounded-lg bg-transparent outline-hidden focus:ring-0 focus:ring-offset-0">
          <SelectValue placeholder="Select a Status" />
        </SelectTrigger>

        <SelectContent>
          <SelectItem v-for="status in statuses" :value="status.value" :key="status.id">
            {{ status.title }}
          </SelectItem>
        </SelectContent>
      </Select>
    </div>

    <CardContent class="ps-2">
      <TimelineItem
        :date="order.createAt"
        name="Order Placed"
        description="Your order has been successfully submitted." />

      <TimelineItem
        :date="order.createAt"
        name="Order Processing"
        description="Once the order is received, it goes through the processing stage. During this time, the items are gathered, and the order is prepared for shipment." />

      <!-- IF ORDER IS READY TO SHIPPED -->
      <TimelineItem
        v-if="order.status === 'Shipped' || order.status === 'Delivered'"
        :date="order.createAt"
        name="Shipped Order"
        description="The order is shipped out to the customer's designated delivery address." />

      <TimelineItem
        v-if="order.status === 'Shipped' || order.status === 'Delivered'"
        :date="order.createAt"
        name="Out for Delivery"
        description="This status indicates that the order is currently out for delivery by the shipping or courier company." />

      <!-- IF ORDER IS DELIVERED -->
      <TimelineItem
        v-if="order.status === 'Delivered'"
        :date="order.createAt"
        name="Delivered"
        description="Finally, when the order successfully reaches the customer's address and is handed over, the status changes to Delivered." />
    </CardContent>
  </Card>
</template>
