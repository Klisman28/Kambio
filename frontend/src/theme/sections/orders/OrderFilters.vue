<script setup lang="ts">
// SHADCN COMPONENTS
import {
  Select,
  SelectItem,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/theme/components/ui/select";
import { Input } from "@/theme/components/ui/input";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// DATA STORE
import { useOrders } from "@/theme/stores/orders";
// CUSTOM COMPOSABLE
import { useOrderStatuses } from "./hooks/useOrderStatuses";
import { usePaymentMethods } from "./hooks/usePaymentMethods";

const { state } = useOrders();
const { statuses } = useOrderStatuses();
const { paymentMethods } = usePaymentMethods();
</script>

<template>
  <div class="flex flex-col justify-between gap-4 pt-6 mb-6 md:flex-row md:items-center">
    <div class="flex flex-col items-center w-full gap-3 md:flex-row lg:w-2/4">
      <div class="relative w-full">
        <Input
          type="search"
          placeholder="Find Order"
          class="rounded-lg ps-9"
          v-model="state.filters.search" />
        <Icon
          :size="18"
          name="Search"
          :strokeWidth="2"
          class="absolute inset-y-0 my-auto text-muted start-3" />
      </div>

      <div class="flex flex-col items-center w-full gap-3 md:flex-row">
        <Select v-model="state.filters.status">
          <SelectTrigger>
            <SelectValue placeholder="Select a Status" />
          </SelectTrigger>

          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem v-for="status in statuses" :key="status.id" :value="status.value">
              {{ status.title }}
            </SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="state.filters.payment">
          <SelectTrigger>
            <SelectValue placeholder="Select a Payment" />
          </SelectTrigger>

          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem :key="payment.id" :value="payment.value" v-for="payment in paymentMethods">
              {{ payment.title }}
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  </div>
</template>
