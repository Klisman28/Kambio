<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
// TYPES
import { Invoice } from "@/types/Invoice";

const { invoice } = defineProps<{ invoice: Invoice }>();
</script>

<template>
  <Card class="self-start p-6 col-span-full xl:col-span-4">
    <CardContent class="space-y-12">
      <div>
        <h5 class="mb-4 text-sm font-semibold">Payment Details</h5>

        <div class="space-y-3">
          <p class="mb-2 text-sm font-semibold">
            Payment Method:
            <span class="text-sm font-medium text-muted">
              {{ invoice.payment.paymentMethod }}
            </span>
          </p>

          <p class="mb-2 text-sm font-semibold">
            Card Holder:
            <span class="text-sm font-medium text-muted">
              {{ invoice?.payment.cardHolder }}
            </span>
          </p>

          <p class="mb-2 text-sm font-semibold">
            Card Number:
            <span class="text-sm font-medium text-muted">
              {{ invoice?.payment.cardNo }}
            </span>
          </p>

          <p class="mb-2 text-sm font-semibold">
            Total Amount:
            <span class="text-sm font-medium text-muted">{{ invoice.totalAmount }} </span>
          </p>
        </div>
      </div>

      <div>
        <h5 class="mb-4 text-sm font-semibold">Project Overview</h5>
        <div class="space-y-3">
          <div class="flex items-center gap-2">
            <p class="text-sm font-semibold">Project Name:</p>
            <Button variant="link">View Project</Button>
          </div>

          <p class="mb-2 text-sm font-semibold">
            Completed By:
            <span class="text-sm font-medium text-muted">Bit Skyber</span>
          </p>

          <p class="mb-2 text-sm font-semibold">
            Time Spent:
            <span class="text-sm font-medium text-muted">120 Hours. $20/Hour Rate </span>
          </p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
