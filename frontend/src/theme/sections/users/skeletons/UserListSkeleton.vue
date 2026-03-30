<script setup lang="ts">
import { TableRow, TableCell } from "@/components/ui/table";
</script>

<template>
  <TableRow class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border animate-pulse">
    <TableCell>
      <div class="h-2 rounded-full bg-skeleton"></div>
    </TableCell>

    <TableCell>
      <div class="flex items-center gap-2">
        <div class="shrink-0 w-10 h-10 rounded-md bg-skeleton"></div>
        <div class="w-full">
          <p class="w-full h-2 mb-1 rounded-full bg-skeleton"></p>
          <p class="w-10 h-2 rounded-full bg-skeleton"></p>
        </div>
      </div>
    </TableCell>

    <TableCell><div class="h-2 rounded-full bg-skeleton"></div></TableCell>
    <TableCell><div class="h-2 rounded-full bg-skeleton"></div></TableCell>
    <TableCell><div class="h-2 rounded-full bg-skeleton"></div></TableCell>
    <TableCell><div class="h-2 rounded-full bg-skeleton"></div></TableCell>
    <TableCell><div class="h-2 rounded-full bg-skeleton"></div></TableCell>
    <TableCell>
      <div class="mx-auto rounded-md w-7 h-7 bg-skeleton"></div>
    </TableCell>
  </TableRow>
</template>
