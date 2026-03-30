<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useField } from "vee-validate";
import axios from "axios";
// SHADCN COMPONENTS
import { Label } from "@/components/ui/label";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
// TYPES
type Size = { id: number; title: string; value: string };

const { value, errorMessage, handleChange } = useField<string[]>("sizes");

const sizes = ref<Size[]>([]);
const isLoading = ref(false);

const getProductSizes = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Size[]>("/api/products/sizes");
    if (data) sizes.value = data;
  } catch (err) {
    console.log(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(getProductSizes);
</script>

<template>
  <div>
    <Label for="sizes" class="inline-block mb-3 text-sm font-medium">Sizes</Label>

    <div class="flex flex-wrap items-center gap-4">
      <!-- SHOW LOADING SPINNER -->
      <div
        v-if="isLoading"
        v-for="item in 5"
        :key="item"
        class="rounded-md animate-pulse size-8 bg-skeleton"></div>

      <ToggleGroup
        v-if="!isLoading && sizes.length"
        type="multiple"
        class="inline-flex gap-2"
        :model-value="value"
        @update:model-value="handleChange">
        <ToggleGroupItem
          v-for="size in sizes"
          :key="size.id"
          :value="size.value"
          class="!data-[state=on]:text-main size-8 text-xs uppercase">
          {{ size.title }}
        </ToggleGroupItem>
      </ToggleGroup>
    </div>

    <span
      role="alert"
      v-if="errorMessage"
      class="inline-block mt-2 ml-2 text-xs font-medium text-red-500">
      {{ errorMessage }}
    </span>
  </div>
</template>
