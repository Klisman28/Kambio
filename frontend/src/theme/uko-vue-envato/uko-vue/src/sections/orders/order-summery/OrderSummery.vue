<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
// CUSTOM COMPONENT
import TableRowItem from "./TableRowItem.vue";
// CUSTOM UTILS METHOD
import { currency } from "@/lib/currency";
// TYPES
import { Order } from "@/types/Order";

defineProps<{ order: Order }>();
</script>

<template>
  <Card class="pt-5">
    <CardTitle class="px-5 mb-4 text-base">Order Summary</CardTitle>

    <Table>
      <TableBody>
        <TableRow v-for="item in order.items" :key="item.id">
          <TableCell>
            <div class="flex items-center gap-3">
              <Avatar shape="square">
                <AvatarImage :src="item.image" :alt="item.name" />
                <AvatarFallback>{{ item.name[0] }}</AvatarFallback>
              </Avatar>

              <div>
                <p>{{ item.name }}</p>
                <p class="pt-1 text-xs text-muted">
                  {{ currency(item.price) }} x {{ item.quantity }}
                </p>
              </div>
            </div>
          </TableCell>

          <TableCell class="text-end!">{{ currency(item.price * item.quantity) }}</TableCell>
        </TableRow>
      </TableBody>
    </Table>

    <Table class="mt-4">
      <TableBody>
        <TableRowItem name="Sub Total" :value="order.subTotalAmount" />
        <TableRowItem name="Estimated Tax" :value="order.taxAmount" />
        <TableRowItem name="Item Discounts" :value="order.discountAmount" />
        <TableRowItem name="Shipping Charge" :value="order.shippingChargeAmount" />
        <TableRowItem isLast name="Total Amount (USD)" :value="order.totalAmount" />
      </TableBody>
    </Table>
  </Card>
</template>
