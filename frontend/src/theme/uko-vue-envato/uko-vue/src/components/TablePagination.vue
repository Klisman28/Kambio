<script setup lang="ts">
// SHADCN COMPONENTS
import {
  Pagination,
  PaginationLast,
  PaginationList,
  PaginationPrev,
  PaginationNext,
  PaginationFirst,
  PaginationEllipsis,
  PaginationListItem
} from "@/components/ui/pagination";
import { Button } from "@/components/ui/button";

// ==============================================================
interface Props {
  total: number;
  lastIndex: number;
  firstIndex: number;
  //   currentPage: number;
  itemsPerPage?: number;
}
// ==============================================================

withDefaults(defineProps<Props>(), { itemsPerPage: 10 });

const model = defineModel<number>({ default: 1 });
</script>

<template>
  <div class="flex flex-col-reverse items-center gap-4 m-4 px-7 sm:flex-row sm:justify-between">
    <p class="text-sm text-muted">
      Showing <span class="font-medium">{{ firstIndex + 1 }}</span> to
      <span class="font-medium">{{ lastIndex }}</span> of
      <span class="font-medium">{{ total }}</span> entries
    </p>

    <Pagination
      show-edges
      v-slot="{ page }"
      v-model:page="model"
      :total="total"
      :items-per-page="itemsPerPage">
      <PaginationList v-slot="{ items }" class="flex items-center gap-3">
        <PaginationFirst class="border-none rtl:rotate-180" />
        <PaginationPrev class="border-none rtl:rotate-180" />

        <template v-for="(item, index) in items">
          <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
            <Button
              class="w-8 h-8 p-0 border-none"
              :variant="item.value === page ? 'default' : 'outline'">
              {{ item.value }}
            </Button>
          </PaginationListItem>

          <PaginationEllipsis v-else :key="item.type" :index="index" />
        </template>

        <PaginationNext class="border-none rtl:rotate-180" />
        <PaginationLast class="border-none rtl:rotate-180" />
      </PaginationList>
    </Pagination>
  </div>
</template>
