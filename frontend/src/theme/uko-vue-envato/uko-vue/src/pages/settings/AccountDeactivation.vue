<script setup lang="ts">
// SHADCN COMPONENTS
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardTitle } from "@/components/ui/card";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle>Account Deactivation</CardTitle>
    <p class="mt-2 mb-6 text-sm text-muted">
      When you initiate the account deletion process, you'll no longer have access to Front account
      services, and your personal data will be permanently removed. You have a 10-day window to
      cancel the deletion if needed.
    </p>

    <div class="space-y-5">
      <form class="space-y-8">
        <div class="flex items-center gap-2">
          <Checkbox id="terms" />
          <Label for="terms" class="text-sm font-medium">
            Confirm that I want to delete my account.
          </Label>
        </div>

        <div class="flex gap-4">
          <Button color="success" class="px-5">Learn More</Button>
          <Button class="px-8">Save</Button>
        </div>
      </form>
    </div>
  </Card>
</template>
