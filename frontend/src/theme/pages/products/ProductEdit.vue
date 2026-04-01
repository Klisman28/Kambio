<script setup lang="ts">
import { useRoute } from "vue-router";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// SECTION COMPONENTS
import ProductForm from "@/theme/sections/products/product-form";
import { ProductFormSkeleton } from "@/theme/sections/products/skeletons";
// CUSTOM COMPOSABLE
import { useProduct } from "@/theme/hooks/useProduct";

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
