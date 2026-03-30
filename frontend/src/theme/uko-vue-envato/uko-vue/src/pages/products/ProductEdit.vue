<script setup lang="ts">
import { useRoute } from "vue-router";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// SECTION COMPONENTS
import ProductForm from "@/sections/products/product-form";
import { ProductFormSkeleton } from "@/sections/products/skeletons";
// CUSTOM COMPOSABLE
import { useProduct } from "@/hooks/useProduct";

const route = useRoute();
const { isLoading, product } = useProduct(+route.params.id);
</script>
<template>
  <Card class="max-w-(--breakpoint-lg) p-6 mx-auto mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Edit Product</CardTitle>

    <!-- SHOW LOADING SKELETON -->
    <ProductFormSkeleton v-if="isLoading" />

    <!-- PRODUCT FORM WITH DATA -->
    <ProductForm v-if="!isLoading && product" :product="product" />
  </Card>
</template>
