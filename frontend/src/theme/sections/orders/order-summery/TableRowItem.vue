<script setup lang="ts">
import { TableCell, TableRow } from "@/theme/components/ui/table";
// CUSTOM UTILS METHODS
import { cn } from "@/theme/lib/utils";
import { currency } from "@/theme/lib/currency";

defineProps<{ name: string; value: number; isLast?: boolean }>();
</script>

<template>
  <TableRow
    :class="
      cn({
        '[&>td:last-of-type]:text-end': true,
        '[&>td]:font-normal [&>td]:border-b [&>td]:border-border': !isLast,
        '[&>td]:font-bold [&>td]:text-foreground': isLast
      })
    ">
    <TableCell class="py-3 text-muted">{{ name }}</TableCell>
    <TableCell class="py-3">{{ currency(value) }}</TableCell>
  </TableRow>
</template>
