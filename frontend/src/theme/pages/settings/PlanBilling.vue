<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import TextField from "@/components/form/TextField.vue";
import PlanItem from "@/sections/settings/PlanItem.vue";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle class="mb-6 text-base leading-none">Plan & Billing</CardTitle>

    <CardContent>
      <div class="space-y-5">
        <h5 class="text-sm font-semibold">Change your plan</h5>

        <Alert>
          <AlertTitle class="flex items-center gap-2 font-normal leading-normal">
            <Icon name="MessageCircleWarning" :size="21" :strokeWidth="2" class="shrink-0" />
            Changing the plan will take effect immediately. You will be charged for the rest of the
            current month.
          </AlertTitle>
        </Alert>

        <!-- Subscription Plan -->
        <div class="grid grid-cols-1 gap-4 xl:gap-6 md:grid-cols-3">
          <PlanItem :price="10" name="Basic" description="Starter Plan for Individuals" isCurrent />
          <PlanItem :price="20" name="Premium" description="Starter Plan for Individuals" />
          <PlanItem :price="30" name="Enterprise" description="Starter Plan for Individuals" />
        </div>
      </div>

      <hr class="my-10 border-border" />

      <!-- Payment Details -->
      <div class="space-y-5">
        <h5 class="text-sm font-semibold">Payment Details</h5>

        <form class="space-y-8">
          <div class="grid grid-cols-4 gap-4 xl:gap-6">
            <div class="col-span-full">
              <TextField
                id="card-holder"
                name="card-holder"
                label="Card Holder"
                placeholder="John Doe" />
            </div>

            <div class="col-span-full sm:col-span-2">
              <TextField
                id="card-number"
                name="card-number"
                label="Card Number"
                placeholder="4242 4242 4242 4242" />
            </div>

            <div class="col-span-2 sm:col-auto">
              <TextField
                id="expiration-date"
                name="expiration-date"
                label="Expiry date"
                placeholder="11/26" />
            </div>

            <div class="col-span-2 sm:col-auto">
              <TextField id="cvc" name="cvc" label="CVC" placeholder="4356" />
            </div>

            <div class="col-span-2">
              <TextField id="country" name="country" label="Country" placeholder="USA" />
            </div>

            <div class="col-span-2">
              <TextField
                id="postal-code"
                name="postal-code"
                label="Postal code"
                placeholder="42345" />
            </div>
          </div>

          <div class="flex gap-4">
            <Button color="error" class="px-6">Cancel</Button>
            <Button class="px-8">Save</Button>
          </div>
        </form>
      </div>
    </CardContent>
  </Card>
</template>
