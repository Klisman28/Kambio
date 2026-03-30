<script setup lang="ts">
// SHADCN COMPONENTS
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectItem,
  SelectValue,
  SelectContent,
  SelectTrigger
} from "@/components/ui/select";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
// SECTION COMPONENTS
import ProductList from "@/sections/products/ProductList.vue";
// STORE
import { useProducts } from "@/stores/products";

const { state } = useProducts();
</script>

<template>
  <!-- PRODUCT TABLE FILTER ACTIONS -->
  <div class="flex flex-col justify-between gap-4 mt-2 mb-6 md:flex-row md:items-center">
    <div class="flex flex-col items-center gap-3 md:flex-row md:w-3/4 lg:w-2/4">
      <div class="relative w-full">
        <Input
          v-model="state.filters.search"
          type="search"
          placeholder="Find Product"
          class="rounded-lg ps-9" />
        <Icon
          :size="18"
          name="Search"
          :strokeWidth="2"
          class="absolute inset-y-0 my-auto text-muted start-3" />
      </div>

      <Select v-model="state.filters.status">
        <SelectTrigger>
          <SelectValue placeholder="Select a Status" />
        </SelectTrigger>

        <SelectContent>
          <SelectItem value="all">All</SelectItem>
          <SelectItem value="published">Published</SelectItem>
          <SelectItem value="draft">Draft</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <Button @click="$router.push('/products/create')">
      <Icon name="Plus" :strokeWidth="2" :size="18" class="me-2" />
      Add Product
    </Button>
  </div>

  <!-- PRODUCT TABLE -->
  <ProductList />
</template>
