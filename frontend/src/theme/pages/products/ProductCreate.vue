<script setup lang="ts">
// SHADCN COMPONENT
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import ProductForm from "@/theme/sections/products/product-form";
</script>

<template>
  <Card class="max-w-(--breakpoint-lg) p-6 mx-auto mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Add Product</CardTitle>
    <ProductForm />
  </Card>
</template>
