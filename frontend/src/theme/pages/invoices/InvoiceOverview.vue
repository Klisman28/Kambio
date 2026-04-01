<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
// CUSTOM COMPONENTS
import InvoicePreview from "@/theme/sections/invoices/InvoicePreview.vue";
import InvoicePayment from "@/theme/sections/invoices/InvoicePayment.vue";
import { InvoiceOverviewSkeleton } from "@/theme/sections/invoices/skeletons";
// TYPES
import { Invoice } from "@/theme/types/Invoice";

const route = useRoute();
const router = useRouter();

const error = ref();
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
  <!-- SHOW LOADING SKELETON -->
  <InvoiceOverviewSkeleton v-if="isLoading" />

  <!-- SHOW PAGE WHEN DATA IS LOADED -->
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7" v-if="!isLoading && invoice">
    <InvoicePreview :invoice="invoice" />
    <InvoicePayment :invoice="invoice" />
  </div>
</template>
