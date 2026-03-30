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
} from "@/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/components/ui/menubar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge, BadgeVariants } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import TablePagination from "@/components/TablePagination.vue";
// USER STORE
import { useInvoices } from "@/stores/invoices";
// CUSTOM UTILS METHODS
import { currency } from "@/lib/currency";
import { dateFormat } from "@/lib/dateFormat";
import { InvoiceListSkeleton } from "./skeletons";

const { state, resetFilter, deleteInvoice } = useInvoices();
const { filters, isLoading, invoices, meta } = toRefs(state);

const getBadgeVariant = (status: string): BadgeVariants["variant"] => {
  const str = status.toLowerCase();
  if (str === "pending") return "default";
  else if (str === "complete") return "success";
};

const tableHeads = ["Customer", "Issue", "Due", "Amount", "Status", "Action"];
</script>

<template>
  <Card class="mb-6">
    <Scrollbar>
      <Table class="min-w-[1200px]">
        <TableHeader>
          <TableRow>
            <TableHead :key="head" v-for="head in tableHeads" class="py-5">{{ head }}</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <!-- SHOW LOADING SKELETON -->
          <InvoiceListSkeleton v-if="isLoading" />

          <!-- NOT FOUND MESSAGE -->
          <TableRow v-else-if="!isLoading && invoices.length === 0">
            <TableCell colspan="8" class="py-24 m-4 text-center bg-slate-200/20">
              <p class="mb-4 text-2xl">No invoices found for '{{ filters.search }}'</p>
              <Button variant="outline" class="rounded-full" @click="resetFilter()">
                Clear your search and try again
              </Button>
            </TableCell>
          </TableRow>

          <!-- SHOW LIST WHEN DATA IS LOADED -->
          <template v-if="!isLoading && invoices.length">
            <TableRow
              v-for="invoice in invoices"
              :id="invoice.id"
              class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border">
              <TableCell>
                <div class="flex gap-3 items-center">
                  <Avatar size="sm" shape="square">
                    <AvatarImage :src="invoice.customer.image" alt="customer" />
                    <AvatarFallback>{{ invoice.customer.name[0] }}</AvatarFallback>
                  </Avatar>

                  <div>
                    <p class="text-sm">{{ invoice.customer.name }}</p>
                    <RouterLink
                      :to="`/invoices/${invoice.id}`"
                      class="pt-1 text-xs text-muted hover:underline">
                      #{{ invoice.id }}
                    </RouterLink>
                  </div>
                </div>
              </TableCell>

              <TableCell>
                {{ dateFormat(invoice.issueDate, "DD MMM YYYY") }}
                <p class="pt-1 text-xs text-muted">{{ dateFormat(invoice.issueDate, "h:mm a") }}</p>
              </TableCell>

              <TableCell>
                {{ dateFormat(invoice.dueDate, "DD MMM YYYY") }}
                <p class="pt-1 text-xs text-muted">{{ dateFormat(invoice.issueDate, "h:mm a") }}</p>
              </TableCell>

              <TableCell>{{ currency(invoice.totalAmount) }}</TableCell>

              <TableCell>
                <Badge class="capitalize" :variant="getBadgeVariant(invoice.status)">
                  {{ invoice.status }}
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
                        :to="`/invoices/${invoice.id}`"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="SquarePen" :size="18" class="text-muted" /> Edit
                      </MenubarItem>

                      <MenubarItem
                        :as="RouterLink"
                        :to="`/invoices/${invoice.id}/details`"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                        <Icon name="Eye" :size="18" class="text-muted" /> View
                      </MenubarItem>

                      <MenubarItem
                        @click="deleteInvoice(invoice.id)"
                        class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
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

    <!-- INVOICE TABLE PAGINATION -->
    <TablePagination
      v-if="invoices.length > 0"
      :total="meta.total"
      :lastIndex="meta.lastIndex"
      :firstIndex="meta.firstIndex"
      v-model="filters.currentPage" />
  </Card>
</template>
