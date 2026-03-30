<script setup lang="ts">
import { TableRow, TableCell } from "@/components/ui/table";
</script>

<template>
  <TableRow
    v-for="i in 10"
    :key="i"
    class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border animate-pulse">
    <TableCell>
      <div class="h-2 rounded-full bg-skeleton"></div>
    </TableCell>
    <TableCell>
      <div class="h-2 rounded-full bg-skeleton"></div>
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
