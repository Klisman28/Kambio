<script setup lang="ts">
import { type HTMLAttributes, computed } from "vue";
import { SelectIcon, SelectTrigger, type SelectTriggerProps, useForwardProps } from "radix-vue";
import { ChevronDown } from "lucide-vue-next";
import { cn } from "@/theme/lib/utils";

const props = defineProps<SelectTriggerProps & { class?: HTMLAttributes["class"] }>();

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});

const forwardedProps = useForwardProps(delegatedProps);
</script>

<template>
  <SelectTrigger
    v-bind="forwardedProps"
    :class="
      cn(
        'flex w-full items-center justify-between rounded-lg bg-card text-card-foreground border border-border p-3 text-sm ring-offset-background focus:outline-hidden focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1',
        props.class
      )
    ">
    <slot />
    <SelectIcon as-child>
      <ChevronDown class="w-4 h-4 opacity-50" />
    </SelectIcon>
  </SelectTrigger>
</template>
