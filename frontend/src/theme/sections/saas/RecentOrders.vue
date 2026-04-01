<script setup lang="ts">
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import {
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
import { Badge } from "@/theme/components/ui/badge";
import { Card, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// CUSTOM DATA
import { recentOrders } from "@/theme/data/dashboards/sass";
// CUSTOM UTILS METHOD
import { currency } from "@/theme/lib/currency";
</script>

<template>
  <Card class="pt-6 col-span-full xl:col-span-8">
    <CardTitle class="px-5 mb-6">Recent Order</CardTitle>

    <Scrollbar>
      <Table class="min-w-[800px]">
        <TableHeader>
          <TableRow>
            <TableHead>Tracking No</TableHead>
            <TableHead>Product Name</TableHead>
            <TableHead>Price</TableHead>
            <TableHead>Total Order</TableHead>
            <TableHead>Total amount</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <TableRow v-for="order in recentOrders" :key="order.id">
            <TableCell>
              {{ order.trackingNo }}
            </TableCell>

            <TableCell>
              <div class="flex items-center gap-2">
                <Avatar shape="square" class="w-8 h-8">
                  <AvatarImage :src="order.img" alt="product" />
                  <AvatarFallback>{{ order.productName }}</AvatarFallback>
                </Avatar>

                <p>{{ order.productName }}</p>
              </div>
            </TableCell>

            <TableCell>{{ currency(order.price, 0) }}</TableCell>

            <TableCell>
              <Badge>{{ order.totalOrder }}</Badge>
            </TableCell>

            <TableCell>{{ currency(order.totalAmount, 0) }}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Scrollbar>
  </Card>
</template>
