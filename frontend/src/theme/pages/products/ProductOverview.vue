<script setup lang="ts">
import { useRoute } from "vue-router";
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
// SECTION COMPONENTS
import ProductReview from "@/sections/products/ProductReview.vue";
import ProductDetails from "@/sections/products/ProductDetails.vue";
// CUSTOM COMPOSABLE
import { useProduct } from "@/hooks/useProduct";
// CUSTOM UTILS METHODS
import { cn } from "@/lib/utils";
import { ProductOverviewSkeleton } from "@/sections/products/skeletons";

const route = useRoute();
const { isLoading, product } = useProduct(+route.params.id);
</script>

<template>
  <div class="grid grid-cols-12 mt-4 mb-6 gap-7">
    <div class="col-span-full 2xl:col-span-4 xl:col-span-5">
      <Card class="sticky p-6 top-24">
        <div class="grid grid-cols-1 gap-5 md:grid-cols-12">
          <!-- SHOW LOADING SKELETONS -->
          <template v-if="isLoading">
            <div
              class="w-full h-full rounded-md md:col-span-8 md:row-span-2 bg-skeleton animate-pulse"></div>

            <div
              v-for="i in 5"
              :key="i"
              class="rounded-md size-28 md:col-span-4 bg-skeleton animate-pulse"></div>
          </template>

          <!-- SHOW PRODUCT IMAGES WHEN AVAILABLE -->
          <template v-if="!isLoading && product">
            <div
              v-for="(image, index) in product.images"
              :class="
                cn({
                  'rounded-md md:col-span-8 md:row-span-2 bg-slate-100 dark:bg-slate-900/40':
                    index === 0,
                  'rounded-md md:col-span-4 bg-slate-100 dark:bg-slate-900/40': index > 0
                })
              ">
              <img :src="image" alt="product" />
            </div>
          </template>
        </div>

        <div class="flex flex-wrap justify-between gap-3 pt-8">
          <Button class="w-full" size="lg" variant="outline">Add to Cart</Button>
          <Button class="w-full" size="lg">Buy Now</Button>
        </div>

        <div class="flex flex-col items-center justify-center gap-1 pt-6 sm:flex-row sm:gap-8">
          <button class="inline-flex items-center h-10 text-sm font-medium hover:text-primary">
            <Icon name="ArrowRightLeft" :size="18" class="me-2" />
            <span>Compare</span>
          </button>

          <button
            class="inline-flex items-center h-10 text-sm font-medium whitespace-nowrap hover:text-primary">
            <Icon name="CircleHelp" :size="18" class="me-2" />
            <span>Ask a Question</span>
          </button>

          <button class="inline-flex items-center h-10 text-sm font-medium hover:text-primary">
            <Icon name="Share2" :size="18" class="me-2" />
            <span>Share</span>
          </button>
        </div>
      </Card>
    </div>

    <!-- RIGHT CARD -->
    <Card class="p-6 col-span-full 2xl:col-span-8 xl:col-span-7">
      <!-- SHOW LOADING SKELETON -->
      <ProductOverviewSkeleton v-if="isLoading" />

      <CardContent class="space-y-5" v-if="!isLoading && product">
        <!-- PRODUCT DETAILS -->
        <ProductDetails :product="product" />

        <!-- PRODUCT REVIEWS -->
        <ProductReview :product="product" />
      </CardContent>
    </Card>
  </div>
</template>
