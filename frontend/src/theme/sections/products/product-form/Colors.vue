<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useField } from "vee-validate";
import axios from "axios";
// SHADCN COMPONENT
import { Label } from "@/components/ui/label";
// TYPES
type Color = { id: number; title: string; value: string };

const { value, errorMessage } = useField<string[]>("colors");

const colors = ref<Color[]>([]);
const isLoading = ref(false);

const getProductColors = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Color[]>("/api/products/colors");
    if (data) colors.value = data;
  } catch (err) {
    console.log(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(getProductColors);
</script>

<template>
  <div>
    <Label for="colors" class="inline-block mb-3 text-sm font-medium">Colors</Label>

    <div class="flex flex-wrap items-center gap-3">
      <!-- SHOW LOADING SPINNER -->
      <div
        v-if="isLoading"
        v-for="item in 5"
        :key="item"
        class="rounded-md animate-pulse size-6 bg-skeleton"></div>

      <!-- SHOW COLORS INPUTS -->
      <input
        v-else
        v-for="color in colors"
        :value="color.value"
        :key="color.id"
        name="colors"
        type="checkbox"
        v-model="value"
        class="inline-block align-middle rounded-xs appearance-none cursor-pointer ring-1 ring-transparent ring-offset-background ring-offset-1 size-5 disabled:opacity-75 disabled:cursor-default"
        :class="{
          'bg-sky-500 border-sky-500 checked:ring-sky-500': color.value === 'blue',
          'bg-orange-500 border-orange-500 checked:ring-orange-500': color.value === 'orange',
          'bg-red-500 border-red-500 checked:ring-red-500': color.value === 'red',
          'bg-green-500 border-green-500 checked:ring-green-500': color.value === 'green',
          'bg-purple-500 border-purple-500 checked:ring-purple-500': color.value === 'purple',
          'bg-pink-500 border-pink-500 checked:ring-pink-500': color.value === 'pink'
        }" />
    </div>

    <span
      role="alert"
      v-if="errorMessage"
      class="inline-block mt-2 ml-2 text-xs font-medium text-red-500">
      {{ errorMessage }}
    </span>
  </div>
</template>
