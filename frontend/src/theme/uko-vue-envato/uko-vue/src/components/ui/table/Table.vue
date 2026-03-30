<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { cn } from "@/lib/utils";

const props = defineProps<{ class?: HTMLAttributes["class"] }>();
</script>

<template>
  <table :class="cn('w-full caption-bottom font-medium text-sm', props.class)">
    <slot />
  </table>
</template>
