<script setup lang="ts">
import { type HTMLAttributes, computed } from "vue";
import type { CheckboxRootEmits, CheckboxRootProps } from "radix-vue";
import { CheckboxIndicator, CheckboxRoot, useForwardPropsEmits } from "radix-vue";
import { Check } from "lucide-vue-next";
import { cn } from "@/theme/lib/utils";

const props = defineProps<CheckboxRootProps & { class?: HTMLAttributes["class"] }>();
const emits = defineEmits<CheckboxRootEmits>();

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});

const forwarded = useForwardPropsEmits(delegatedProps, emits);
</script>

<template>
  <CheckboxRoot
    v-bind="forwarded"
    :class="
      cn(
        'peer h-[21px] w-[21px] shrink-0 rounded-md border-2 border-primary ring-offset-background focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-white',
        props.class
      )
    ">
    <CheckboxIndicator class="flex items-center justify-center w-full h-full text-current">
      <slot>
        <Check class="w-4 h-4" />
      </slot>
    </CheckboxIndicator>
  </CheckboxRoot>
</template>
