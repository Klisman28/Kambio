<script setup lang="ts">
import { toRefs } from "vue";
import { RouterLink } from "vue-router";
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import {
  Table,
  TableRow,
  TableCell,
  TableBody,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/theme/components/ui/menubar";
import { Card } from "@/theme/components/ui/card";
import { Badge } from "@/theme/components/ui/badge";
import { Button } from "@/theme/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// CUSTOM COMPONENTS
import { ProductListSkeleton } from "./skeletons";
import Icon from "@/theme/components/Icon.vue";
import TablePagination from "@/theme/components/TablePagination.vue";
// USER STORE
import { useProducts } from "@/theme/stores/products";
// CUSTOM UTILS METHOD
import { currency } from "@/theme/lib/currency";

const { state, deleteProduct, resetFilter } = useProducts();
const { filters, meta, products, isLoading } = toRefs(state);

const tableHead = ["Product", "Created At", "Price", "Stock", "Status", "Action"];
</script>

<template>
  <Card class="mb-6">
    <Scrollbar>
      <!-- Product Table -->
      <Table class="min-w-[1200px]">
        <TableHeader>
          <TableRow>
            <TableHead v-for="head in tableHead" :key="head" class="px-8 py-5">
              {{ head }}
            </TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <!-- LOADING SKELETON -->
          <template v-if="isLoading">
            <ProductListSkeleton v-for="i in 10" :key="i" />
          </template>

          <!-- NOT FOUND PRODUCT MESSAGE -->
          <TableRow v-if="!isLoading && products.length === 0">
            <TableCell colspan="8" class="py-24 m-4 text-center bg-slate-200/20">
              <p class="mb-4 text-2xl">No products found for {{ filters.search }}</p>
              <Button variant="outline" class="rounded-full" @click="resetFilter()">
                Clear your search and try again
              </Button>
            </TableCell>
          </TableRow>

          <template v-if="!isLoading && products.length > 0">
            <TableRow
              v-for="product in products"
              :key="product.id"
              class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border">
              <TableCell>
                <div class="flex gap-3 items-center">
                  <Avatar shape="square">
                    <AvatarImage :src="product.featureImage" alt="Product" />
                    <AvatarFallback>P</AvatarFallback>
                  </Avatar>

                  <div>
                    <RouterLink :to="`/products/${product.id}`">
                      <p class="font-medium hover:underline">{{ product.title }}</p>
                    </RouterLink>

                    <span class="text-xs text-muted">
                      {{ product.category }}
                    </span>
                  </div>
                </div>
              </TableCell>

              <TableCell>{{ product.createdAt }}</TableCell>
              <TableCell>{{ currency(product.price) }}</TableCell>
              <TableCell>
                <p
                  :class="{
                    'text-error': product.stock < 5,
                    'text-success': product.stock > 20,
                    'text-warning': product.stock < 20 && product.stock > 5
                  }">
                  {{ product.stock }}
                </p>
              </TableCell>

              <TableCell>
                <Badge :variant="product.status === 'Published' ? 'success' : 'warning'">
                  {{ product.status }}
                </Badge>
              </TableCell>

              <TableCell>
                <Menubar class="justify-center p-0 bg-transparent">
                  <MenubarMenu>
                    <MenubarTrigger class="p-1 w-6 h-6 rounded-sm bg-slate-100 dark:bg-slate-800">
                      <Icon name="Ellipsis" :size="18" />
                    </MenubarTrigger>

                    <MenubarContent align="end">
                      <MenubarItem
                        :as="RouterLink"
                        :to="`/products/${product.id}`"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="SquarePen" :size="18" class="text-muted" /> Edit
                      </MenubarItem>

                      <MenubarItem
                        :as="RouterLink"
                        :to="`/products/${product.id}/overview`"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="Eye" :size="18" class="text-muted" /> View
                      </MenubarItem>

                      <MenubarItem
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!"
                        @click="deleteProduct(product.id)">
                        <Icon name="Trash" :size="18" class="text-muted" /> Delete
                      </MenubarItem>
                    </MenubarContent>
                  </MenubarMenu>
                </Menubar>
              </TableCell>
            </TableRow>
          </template>
        </TableBody>
      </Table>
    </Scrollbar>

    <!-- Product Table Pagination -->
    <TablePagination
      v-if="products.length > 0"
      :total="meta.total"
      :lastIndex="meta.lastIndex"
      :firstIndex="meta.firstIndex"
      v-model="filters.currentPage" />
  </Card>
</template>
