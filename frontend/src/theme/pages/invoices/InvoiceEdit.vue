<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// SECTION COMPONENTS
import { InvoiceForm } from "@/theme/sections/invoices/invoice-form";
import { InvoiceFormSkeleton } from "@/theme/sections/invoices/skeletons";
// TYPES
import { Invoice } from "@/theme/types/Invoice";

const route = useRoute();
const router = useRouter();

const error = ref("");
const isLoading = ref(false);
const invoice = ref<Invoice>();

const getInvoice = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Invoice>("/api/invoices", {
      params: { id: route.params.id }
    });

    if (data) invoice.value = data;
    else router.push({ name: "NotFound" });
  } catch (err) {
    error.value = "Something went wrong";
  } finally {
    isLoading.value = false;
  }
};

onMounted(getInvoice);
</script>
<template>
  <Card class="p-6 mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Update Invoice</CardTitle>
    <!-- SHOW LOADING SKELETON -->
    <InvoiceFormSkeleton v-if="isLoading" />

    <!-- INVOICE FORM WITH DATA -->
    <InvoiceForm v-if="!isLoading && invoice" :invoice="invoice" />
  </Card>
</template>
