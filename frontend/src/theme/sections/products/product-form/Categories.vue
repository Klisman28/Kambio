<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
// SHADCN COMPONENT
import { SelectItem } from "@/theme/components/ui/select";
// CUSTOM COMPONENT
import SelectField from "@/theme/components/form/SelectField.vue";
// TYPES
type Category = { id: number; title: string; value: string };

const isLoading = ref(false);
const categories = ref<Category[]>([]);

const getCategories = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Category[]>("/api/products/categories");
    if (data) categories.value = data;
  } catch (err) {
    console.log(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(getCategories);
</script>

<template>
  <SelectField id="category" name="category" label="Category" placeholder="Select category">
    <SelectItem v-for="item in categories" :key="item.id" :value="item.title">
      {{ item.title }}
    </SelectItem>
  </SelectField>
</template>
