<script setup lang="ts">
// SHADCN COMPONENTS
import { CardContent } from "@/theme/components/ui/card";
import { Table, TableBody, TableCell, TableRow } from "@/theme/components/ui/table";
// CUSTOM COMPONENT
import ProductReviewSkeleton from "./ProductReviewSkeleton.vue";
</script>

<template>
  <CardContent class="animate-pulse">
    <div class="h-3 rounded-md w-28 bg-skeleton"></div>

    <div class="mt-4 space-y-4">
      <div class="h-3 rounded-md w-80 bg-skeleton"></div>
      <div class="h-3 rounded-md w-60 bg-skeleton"></div>
      <div class="flex items-center gap-5 mt-2 font-medium">
        <div class="w-32 h-3 rounded-md bg-skeleton"></div>
        <div class="w-24 h-3 rounded-md bg-skeleton"></div>
      </div>
    </div>

    <div class="mt-8 space-y-2" v-for="i in 3" :key="i">
      <div class="w-40 h-3 rounded-md bg-skeleton"></div>
      <div class="h-2 rounded-md w-72 bg-skeleton"></div>
    </div>

    <div class="mt-8">
      <div class="w-40 h-3 mb-4 rounded-md bg-skeleton"></div>

      <div class="space-y-3">
        <div class="h-2 rounded-md bg-skeleton"></div>
        <div class="h-2 rounded-md bg-skeleton"></div>
        <div class="h-2 rounded-md bg-skeleton"></div>
      </div>
    </div>

    <div class="flex flex-wrap gap-4 mt-10">
      <div
        v-for="i in 2"
        :key="i"
        class="flex items-center w-full gap-2 p-4 border rounded-lg border-border sm:max-w-64">
        <div class="rounded-md size-10 bg-skeleton"></div>

        <div class="w-full space-y-1">
          <div class="w-20 h-3 rounded-md bg-skeleton"></div>
          <div class="h-2 rounded-md bg-skeleton"></div>
        </div>
      </div>
    </div>

    <div class="mt-8 space-y-3">
      <div class="w-40 h-3 rounded-md bg-skeleton"></div>
      <div class="h-2 rounded-md bg-skeleton"></div>
      <div class="h-2 rounded-md bg-skeleton"></div>
    </div>

    <div class="mt-8 space-y-3">
      <div class="w-40 h-3 rounded-md bg-skeleton"></div>

      <Table>
        <TableBody>
          <TableRow v-for="i in 3" :key="i" class="[&_td:last-child]:text-left">
            <TableCell class="py-2 border border-border">
              <div class="w-40 h-3 rounded-md bg-skeleton"></div>
            </TableCell>

            <TableCell class="py-2 border border-border">
              <div class="w-40 h-3 rounded-md bg-skeleton"></div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div class="pt-8">
      <div
        class="flex flex-wrap items-center justify-between gap-4 pb-5 mb-5 border-b border-border">
        <div class="w-40 h-3 rounded-md bg-skeleton"></div>
        <div class="w-64 h-2 rounded-md bg-skeleton"></div>
      </div>

      <div class="flex items-center justify-between mb-4">
        <div class="w-40 h-3 rounded-md bg-skeleton"></div>
        <div class="w-40 h-3 rounded-md bg-skeleton"></div>
      </div>

      <ProductReviewSkeleton />
    </div>
  </CardContent>
</template>
