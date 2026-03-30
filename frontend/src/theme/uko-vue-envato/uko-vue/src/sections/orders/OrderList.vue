<script setup lang="ts">
import { toRefs } from "vue";
import { RouterLink } from "vue-router";
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import {
  Table,
  TableRow,
  TableCell,
  TableBody,
  TableHead,
  TableHeader
} from "@/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/components/ui/menubar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge, BadgeVariants } from "@/components/ui/badge";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import TablePagination from "@/components/TablePagination.vue";
import { OrderListSkeleton } from "./skeletons";
// ORDER STORE
import { useOrders } from "@/stores/orders";
// CUSTOM UTILS METHODS
import { cn } from "@/lib/utils";
import { currency } from "@/lib/currency";
import { dateFormat } from "@/lib/dateFormat";

const { resetFilter, deleteOrder, state } = useOrders();
const { filters, meta, orders, isLoading } = toRefs(state);

const statusBadgeColor = (status: string): BadgeVariants["variant"] => {
  let str = status.toLowerCase();
  if (str === "delivered") return "default";
  else if (str === "shipping") return "success";
  else if (str === "new") return "info";
  else if (str === "pending") return "warning";
  else if (str === "return") return "destructive";
};

const tableHeads = [
  { id: 1, title: "Invoice ID" },
  { id: 2, title: "Order Date" },
  { id: 3, title: "Delivery Date" },
  { id: 4, title: "Customer Name" },
  { id: 5, title: "Payment Method" },
  { id: 6, title: "Amount" },
  { id: 7, title: "Delivery Status", align: "center" },
  { id: 8, title: "Action" }
];
</script>

<template>
  <Card class="mb-6">
    <Scrollbar>
      <Table class="min-w-[1200px]">
        <TableHeader>
          <TableRow>
            <TableHead
              v-for="head in tableHeads"
              :key="head.id"
              :class="cn({ 'py-5': true, 'text-center': head.align === 'center' })">
              {{ head.title }}
            </TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <!-- SHOW LOADING SKELETON -->
          <OrderListSkeleton v-if="isLoading" />

          <!-- NOT FOUND ORDERS MESSAGE -->
          <TableRow v-if="!isLoading && orders.length === 0">
            <TableCell colspan="8" class="py-24 m-4 text-center bg-slate-200/20">
              <p class="mb-4 text-2xl">No orders found for '{{ filters.search }}'</p>
              <Button variant="outline" class="rounded-full" @click="resetFilter()">
                Clear your search and try again
              </Button>
            </TableCell>
          </TableRow>

          <!-- SHOW LIST WHEN DATA IS LOADED -->
          <template v-if="!isLoading && orders.length">
            <TableRow
              :id="order.id"
              v-for="order in orders"
              class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border">
              <TableCell>{{ order.invoiceId }}</TableCell>
              <TableCell>{{ dateFormat(order.createAt, "DD MMM YYYY") }}</TableCell>
              <TableCell>{{ dateFormat(order.deliveredAt, "DD MMM YYYY") }}</TableCell>
              <TableCell>{{ order.customer.name }}</TableCell>
              <TableCell>{{ order.payment.paymentMethod }}</TableCell>
              <TableCell>{{ currency(order.totalAmount) }}</TableCell>

              <TableCell class="text-center">
                <Badge :variant="statusBadgeColor(order.status)">
                  {{ order.status }}
                </Badge>
              </TableCell>

              <TableCell>
                <Menubar class="justify-center p-0 bg-transparent">
                  <MenubarMenu>
                    <MenubarTrigger class="p-1 w-6 h-6 rounded-sm bg-slate-100 dark:bg-slate-800">
                      <Icon name="Ellipsis" :size="18" />
                    </MenubarTrigger>

                    <MenubarContent align="end">
                      <MenubarItem
                        :as="RouterLink"
                        :to="`/orders/${order.id}`"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="Eye" :size="18" class="text-muted" /> View
                      </MenubarItem>

                      <MenubarItem
                        @click="deleteOrder(order.id)"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="Trash" :size="18" class="text-muted" /> Delete
                      </MenubarItem>
                    </MenubarContent>
                  </MenubarMenu>
                </Menubar>
              </TableCell>
            </TableRow>
          </template>
        </TableBody>
      </Table>
    </Scrollbar>

    <!-- ORDER TABLE PAGINATION -->
    <TablePagination
      v-if="orders.length > 0"
      :total="meta.total"
      :lastIndex="meta.lastIndex"
      :firstIndex="meta.firstIndex"
      v-model="filters.currentPage" />
  </Card>
</template>
