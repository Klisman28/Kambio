<script setup lang="ts">
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import { Badge } from "@/theme/components/ui/badge";
import { Card, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
import {
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/theme/components/ui/menubar";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
// CUSTOM UTILS METHODS
import { currency } from "@/theme/lib/currency";
// CUSTOM DATA
import { latestOrders } from "@/theme/data/dashboards/analytics";
</script>

<template>
  <Card class="col-span-full pt-6 pb-2 lg:col-span-8">
    <CardTitle class="px-5 mb-5">Latest Orders</CardTitle>

    <Scrollbar>
      <Table class="min-w-[800px]">
        <TableHeader>
          <TableRow>
            <TableHead>Product</TableHead>
            <TableHead>Customer</TableHead>
            <TableHead>Qty.</TableHead>
            <TableHead>Profit</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Action</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <TableRow v-for="order in latestOrders" :key="order.id">
            <TableCell>
              <div class="flex gap-3 items-center">
                <Avatar shape="square">
                  <AvatarImage :src="order.img" alt="order" />
                  <AvatarFallback>{{ order.id }}</AvatarFallback>
                </Avatar>

                <div>
                  <p class="mb-1 text-[13px] font-semibold">{{ order.productName }}</p>
                  <p class="text-xs text-muted">{{ order.productId }}</p>
                </div>
              </div>
            </TableCell>

            <TableCell>{{ order.customer }}</TableCell>
            <TableCell>{{ order.qty }}</TableCell>
            <TableCell>{{ currency(order.profit) }}</TableCell>

            <TableCell>
              <Badge
                class="font-normal"
                :variant="order.status === 'Complete' ? 'success' : 'default'">
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
                    <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                      <Icon name="Eye" :size="18" class="text-muted" /> View
                    </MenubarItem>

                    <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                      <Icon name="Trash" :size="18" class="text-muted" /> Delete
                    </MenubarItem>
                  </MenubarContent>
                </MenubarMenu>
              </Menubar>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Scrollbar>
  </Card>
</template>
