<script setup lang="ts">
import { computed } from "vue";
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import {
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
// CUSTOM UTILS METHODS
import { currency } from "@/theme/lib/currency";
import { dateFormat } from "@/theme/lib/dateFormat";
// TYPES
import { Invoice } from "@/theme/types/Invoice";

// PROPS
const { invoice } = defineProps<{ invoice: Invoice }>();

const printPage = () => {
  window.print();
};

const subtotal = computed(() => {
  return invoice.products.reduce((prev, curr) => prev + curr.total!, 0);
});
</script>

<template>
  <Card class="col-span-full p-6 xl:col-span-8">
    <CardContent class="space-y-10">
      <div class="flex justify-between">
        <div>
          <img src="/logos/uko.png" class="mb-10 w-10" alt="Uko" />

          <h5 class="mb-3 text-sm font-semibold">Bill to:</h5>
          <p class="text-sm font-semibold">{{ invoice.customer.name }}</p>
          <p class="mb-8 text-xs font-medium text-muted">
            {{ invoice.billingAddress?.address }}
          </p>

          <p class="mb-2 text-sm font-semibold">
            Issue Date:
            <span class="text-sm font-medium text-muted">
              {{ dateFormat(invoice.issueDate, "DD MMM YYYY") }}
            </span>
          </p>

          <p class="text-sm font-semibold">
            Due Date:
            <span class="text-sm font-medium text-muted">
              {{ dateFormat(invoice.dueDate, "DD MMM YYYY") }}
            </span>
          </p>
        </div>

        <div class="text-end">
          <h3 class="text-2xl font-semibold">Invoice</h3>
          <p class="text-sm font-medium">{{ dateFormat(invoice.issueDate, "DD MMM YYYY") }}</p>
          <p class="mt-5 text-xs font-medium text-muted">
            45 Roker Terrace <br />
            Latheronwheel<br />
            KW5 8NW, London<br />
            United Kingdom<br />
          </p>
        </div>
      </div>

      <!-- Product List -->
      <Scrollbar>
        <Table class="min-w-[700px]">
          <TableHeader>
            <TableRow>
              <TableHead>No</TableHead>
              <TableHead>Product</TableHead>
              <TableHead class="text-center">Quantity</TableHead>
              <TableHead class="text-center">Discount</TableHead>
              <TableHead class="text-center">Price</TableHead>
              <TableHead class="text-end">Amount</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            <TableRow v-for="item in invoice.products" :key="item.id">
              <TableCell>{{ item.id }}</TableCell>
              <TableCell>
                <p>{{ item.title }}</p>
                <p class="pt-1 text-xs text-muted">
                  Build with Bootstrap, React JS, Angular, Vue etc.
                </p>
              </TableCell>
              <TableCell class="text-center">{{ item.quantity }}</TableCell>
              <TableCell class="text-center">{{ item.discount }}%</TableCell>
              <TableCell class="text-center"> {{ currency(item.price) }} </TableCell>
              <TableCell class="text-end">{{ currency(item.total) }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Scrollbar>

      <!-- Balance -->
      <Table class="flex justify-end w-full">
        <TableBody>
          <TableRow>
            <TableCell class="py-2">Subtotal:</TableCell>
            <TableCell class="py-2 text-end!">
              {{ currency(subtotal) }}
            </TableCell>
          </TableRow>

          <TableRow>
            <TableCell class="py-2">Vat(%): </TableCell>
            <TableCell class="py-2 text-end!">{{ invoice.tax }}%</TableCell>
          </TableRow>

          <TableRow>
            <TableCell class="py-2">Shipping:</TableCell>
            <TableCell class="py-2 text-end!">{{ currency(invoice.shippingCharge!) }}</TableCell>
          </TableRow>

          <TableRow class="text-sm font-semibold bg-slate-100 dark:bg-active">
            <TableCell class="py-2">Total:</TableCell>
            <TableCell class="py-2 text-end!">{{ currency(invoice.totalAmount) }}</TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <!-- Payment Details -->
      <div>
        <h5 class="mb-4 text-sm font-semibold">Payments Details</h5>
        <p class="mb-2 font-semibold">
          Payment Method:
          <span class="font-medium text-muted">
            {{ invoice.payment.paymentMethod }}
          </span>
        </p>

        <p class="mb-2 font-semibold">
          Card Holder:
          <span class="font-medium text-muted">
            {{ invoice.payment.cardHolder }}
          </span>
        </p>

        <p class="mb-2 font-semibold">
          Card Number:
          <span class="font-medium text-muted">
            {{ invoice.payment.cardNo }}
          </span>
        </p>

        <p class="mb-2 font-semibold">
          Total Amount:
          <span class="font-medium text-muted">{{ currency(invoice.totalAmount) }} </span>
        </p>
      </div>

      <div class="flex gap-2 justify-end">
        <Button type="submit"> <Icon name="Save" :size="18" class="me-2" /> PDF</Button>
        <Button type="submit" color="success" @click="printPage">
          <Icon name="Printer" :size="18" class="me-2" /> Print Invoice
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
