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
import { Card, CardContent } from "@/theme/components/ui/card";
</script>

<template>
  <div class="grid grid-cols-12 gap-7 mt-2 mb-6">
    <Card class="col-span-full p-6 xl:col-span-8">
      <CardContent class="space-y-10">
        <div class="flex justify-between">
          <div>
            <img src="/logos/uko.png" class="mb-10 w-10" alt="Uko" />
            <h5 class="mb-3 w-20 h-3 animate-pulse bg-skeleton"></h5>
            <div class="mb-8 space-y-2">
              <div class="w-40 h-2 rounded-md animate-pulse bg-skeleton"></div>
              <div class="w-40 h-1 rounded-md animate-pulse bg-skeleton"></div>
            </div>
            <div class="mb-2 w-52 h-2 rounded-md animate-pulse bg-skeleton"></div>
            <div class="w-52 h-2 rounded-md animate-pulse bg-skeleton"></div>
          </div>

          <div class="space-y-1 text-end">
            <h3 class="text-2xl font-semibold">Invoice</h3>
            <div class="w-20 h-2 rounded-md animate-pulse ms-auto bg-skeleton"></div>
            <div class="pt-6 space-y-3">
              <div
                v-for="i in 4"
                :key="i"
                class="w-40 h-2 rounded-md animate-pulse bg-skeleton"></div>
            </div>
          </div>
        </div>

        <Scrollbar>
          <Table class="min-w-[700px]">
            <TableHeader>
              <TableRow>
                <TableHead>No</TableHead>
                <TableHead>Product</TableHead>
                <TableHead class="text-center">Quantity</TableHead>
                <TableHead class="text-center">Discount</TableHead>
                <TableHead class="text-center">Price</TableHead>
                <TableHead>Amount</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              <TableRow
                v-for="i in 4"
                :key="i"
                class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border animate-pulse">
                <TableCell>
                  <div class="w-8 h-2 rounded-md bg-skeleton"></div>
                </TableCell>

                <TableCell class="space-y-2">
                  <div class="w-full h-2 rounded-md bg-skeleton"></div>
                  <div class="w-full h-1 rounded-md bg-skeleton"></div>
                </TableCell>

                <TableCell class="text-center">
                  <div class="w-full h-1 rounded-md bg-skeleton"></div>
                </TableCell>

                <TableCell class="text-center">
                  <div class="w-full h-1 rounded-md bg-skeleton"></div>
                </TableCell>

                <TableCell class="text-center">
                  <div class="w-full h-1 rounded-md bg-skeleton"></div>
                </TableCell>

                <TableCell class="text-end">
                  <div class="w-full h-1 rounded-md bg-skeleton"></div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Scrollbar>

        <Table class="flex justify-end w-full">
          <TableBody>
            <TableRow v-for="i in 4" :key="i" class="animate-pulse">
              <TableCell class="py-3">
                <div class="w-20 h-2 rounded-full bg-skeleton"></div>
              </TableCell>
              <TableCell class="py-2 text-end!">
                <div class="w-14 h-2 rounded-full bg-skeleton"></div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>

        <div class="space-y-5">
          <h5 class="mb-4 text-sm font-semibold">Payments Details</h5>
          <p v-for="i in 4" :key="i" class="w-60 h-2 rounded-md animate-pulse bg-skeleton"></p>
        </div>

        <div class="flex gap-2 justify-end">
          <div class="w-28 h-10 rounded-md animate-pulse bg-skeleton"></div>
          <div class="w-28 h-10 rounded-md animate-pulse bg-skeleton"></div>
        </div>
      </CardContent>
    </Card>

    <Card class="col-span-full self-start p-6 xl:col-span-4">
      <CardContent class="space-y-12">
        <div>
          <h5 class="mb-4 text-sm font-semibold">Payment Details</h5>
          <div class="space-y-4">
            <p class="w-1/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-2/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-3/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-full h-2 rounded-md animate-pulse bg-skeleton"></p>
          </div>
        </div>

        <div>
          <h5 class="mb-4 text-sm font-semibold">Project Overview</h5>
          <div class="space-y-4">
            <p class="w-1/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-2/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-3/4 h-2 rounded-md animate-pulse bg-skeleton"></p>
            <p class="w-full h-2 rounded-md animate-pulse bg-skeleton"></p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
