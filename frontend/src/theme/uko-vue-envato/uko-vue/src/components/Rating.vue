<script setup lang="ts">
import { computed } from "vue";
import Icon from "./Icon.vue";

// ==============================================================
interface RatingProps {
  rating: number;
  size?: number;
}
// ==============================================================

const props = withDefaults(defineProps<RatingProps>(), { size: 16 });

const remaining = computed(() => 5 - Math.floor(props.rating));
</script>

<template>
  <div class="flex items-center">
    <Icon
      name="Star"
      :size="size"
      class="fill-warning stroke-none"
      v-for="no in Math.floor(rating)"
      :key="no" />

    <Icon name="Star" :size="size" class="text-warning" v-for="no in remaining" :key="no" />
  </div>
</template>
