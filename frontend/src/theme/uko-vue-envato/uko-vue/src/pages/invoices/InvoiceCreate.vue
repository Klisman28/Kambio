<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// SECTION COMPONENTS
import { InvoiceForm } from "@/sections/invoices/invoice-form";
</script>

<template>
  <Card class="p-6 mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Create Invoice</CardTitle>
    <InvoiceForm />
  </Card>
</template>
