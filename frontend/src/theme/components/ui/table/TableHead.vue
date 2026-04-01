<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { cn } from "@/theme/lib/utils";

const props = defineProps<{ class?: HTMLAttributes["class"] }>();
</script>

<template>
  <th
    :class="
      cn(
        'pb-3 px-4 font-medium xl:px-5 text-left align-middle [&:has([role=checkbox])]:pr-0 last:text-center rtl:text-right',
        props.class
      )
    ">
    <slot />
  </th>
</template>
