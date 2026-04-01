<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// SECTION COMPONENTS
import { InvoiceForm } from "@/theme/sections/invoices/invoice-form";
</script>

<template>
  <Card class="p-6 mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Create Invoice</CardTitle>
    <InvoiceForm />
  </Card>
</template>
