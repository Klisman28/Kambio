<script setup lang="ts">
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import { Badge } from "@/theme/components/ui/badge";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
import {
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
// CUSTOM UTILS METHOD
import { currency } from "@/theme/lib/currency";
// CUSTOM DATA
import { popularProducts } from "@/theme/data/dashboards/sales";
</script>

<template>
  <Card class="pt-6 pb-3 col-span-full lg:col-span-8 lg:pb-0">
    <CardTitle class="px-5 mb-6">Popular Products</CardTitle>

    <Scrollbar>
      <CardContent class="text-xs min-w-[800px]">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Product</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Brand</TableHead>
              <TableHead>Price</TableHead>
              <TableHead class="text-center">Status</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            <TableRow :key="product.id" v-for="product in popularProducts">
              <TableCell>
                <div class="flex items-center gap-2">
                  <Avatar shape="square">
                    <AvatarImage :src="product.img" alt="product" />
                    <AvatarFallback>{{ product.productName }}</AvatarFallback>
                  </Avatar>

                  <p class="mb-1 font-semibold">{{ product.productName }}</p>
                </div>
              </TableCell>

              <TableCell>{{ product.date }}</TableCell>
              <TableCell>{{ product.category }}</TableCell>
              <TableCell>{{ product.brand }}</TableCell>
              <TableCell>{{ currency(product.price) }}</TableCell>

              <TableCell class="text-center">
                <Badge :variant="product.status === 'Out of Stock' ? 'destructive' : 'default'">
                  {{ product.status }}
                </Badge>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Scrollbar>
  </Card>
</template>
