<script setup lang="ts">
// SHADCN COMPONENTS
import { Badge } from "@/components/ui/badge";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import Rating from "@/components/Rating.vue";
// CUSTOM UTILS METHODS
import { cn } from "@/lib/utils";
import { currency } from "@/lib/currency";
// TYPES
import { Product } from "@/types/Product";

defineProps<{ product: Product }>();
</script>

<template>
  <Badge>New Arrivals</Badge>

  <div>
    <h5 class="font-bold">
      {{ product.title }}
    </h5>

    <p class="leading-6 text-muted">Category: {{ product.category }}</p>

    <div class="flex items-center gap-5 mt-2 font-medium">
      <div class="flex items-center gap-1">
        <Rating :rating="product.rating" />
        <p class="leading-none">({{ product.totalReviews }})</p>
      </div>

      <p class="leading-none">122 Sold</p>
    </div>
  </div>

  <!-- PRODUCT PRICE -->
  <div>
    <p class="text-sm font-semibold leading-6">Special Price</p>

    <div class="flex items-center gap-4">
      <h4 class="font-semibold text-primary">
        {{ currency(product.price) }}
        <del class="text-sm text-muted" v-if="product.discount">
          {{ currency(product.price + product.discount) }}
        </del>
      </h4>

      <h5 v-if="product.discount" class="text-success">{{ product.discount }}% Off</h5>
    </div>
  </div>

  <!-- PRODUCT COLORS -->
  <div v-if="product.colors && product.colors.length">
    <p class="text-sm font-semibold leading-6">Select Color</p>

    <div class="flex items-center gap-2 mt-2">
      <input
        v-for="color in product.colors"
        type="radio"
        name="color"
        :id="color"
        :class="
          cn({
            'rounded-xs bg-slate-500 checked:ring-slate-500 appearance-none cursor-pointer size-5 ring-0 ring-offset-1 ring-offset-background ring-transparent checked:ring-1 disabled:cursor-default': true,
            'bg-red-500 checked:ring-red-500': color === 'red',
            'bg-blue-500 checked:ring-blue-500': color === 'blue',
            'bg-pink-500 checked:ring-pink-500': color === 'pink',
            'bg-green-500 checked:ring-green-500': color === 'green',
            'bg-orange-500 checked:ring-orange-500': color === 'orange',
            'bg-purple-500 checked:ring-purple-500': color === 'purple'
          })
        " />
    </div>
  </div>

  <!-- PRODUCT SIZES -->
  <div v-if="product.sizes && product.sizes.length">
    <p class="py-2 text-sm font-semibold leading-6">Select Size</p>

    <ToggleGroup type="single" class="inline-flex gap-2" default-value="l">
      <ToggleGroupItem
        class="!data-[state=on]:text-main size-8 text-xs uppercase"
        v-for="size in product.sizes"
        :value="size.toLowerCase()">
        {{ size }}
      </ToggleGroupItem>
    </ToggleGroup>
  </div>

  <!-- PRODUCT OFFERS -->
  <div v-if="product.offers && product.offers.length">
    <p class="pb-3 text-sm font-semibold leading-6 underline">
      Available Offers ({{ product.offers.length }})
    </p>

    <div class="space-y-2">
      <div
        class="flex items-center font-medium"
        v-for="(offer, index) in product.offers"
        :key="index">
        <Icon name="Tag" :size="16" :strokeWidth="2" class="me-2 text-primary shrink-0" />
        <p>{{ offer }}</p>
      </div>
    </div>
  </div>

  <!-- PRODUCT SHIPPING -->
  <div class="flex flex-wrap gap-4 pt-4">
    <div class="flex items-center w-full gap-2 p-4 border rounded-lg border-border sm:max-w-64">
      <Icon name="Truck" :size="26" :strokewidth="2" class="me-2" />

      <div>
        <p class="font-semibold leading-6">Estimated Delivery</p>
        <p class="text-xs text-muted">01-07 Dec, 2024</p>
      </div>
    </div>

    <div class="flex items-center w-full gap-2 p-4 border rounded-lg border-border sm:max-w-64">
      <Icon name="ShoppingCart" :size="26" :strokewidth="2" class="me-2" />

      <div>
        <p class="font-semibold leading-6">Free Shipping & Returns</p>
        <p class="text-xs text-muted">On all orders over $200.00</p>
      </div>
    </div>
  </div>

  <!-- PRODUCT DESCRIPTION -->
  <div class="pt-4">
    <p class="mb-2 text-sm font-semibold underline">Product Description</p>
    <p class="text-xs leading-5 text-muted">
      {{ product.description }}
    </p>
  </div>

  <!-- PRODUCT FEATURES -->
  <div v-if="product.features && product.features.length">
    <p class="pb-3 text-sm font-semibold underline">Features:</p>
    <Table>
      <TableBody>
        <TableRow v-for="feature in product.features" class="[&_td:last-child]:text-left">
          <TableCell class="py-2 border border-border"> {{ feature.name }} </TableCell>
          <TableCell class="py-2 border border-border">{{ feature.value }} </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
