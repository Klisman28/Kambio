<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENT
import TextField from "@/components/form/TextField.vue";
import SecuritySwitchItem from "@/sections/settings/SecuritySwitchItem.vue";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle class="mb-6 text-base leading-none">Change your password</CardTitle>

    <CardContent>
      <form>
        <div class="space-y-9">
          <div class="space-y-5">
            <TextField
              id="currentPassword"
              name="currentPassword"
              label="Current Password"
              placeholder="Current Password" />

            <TextField
              id="newPassword"
              name="newPassword"
              label="New Password"
              placeholder="New Password" />
          </div>

          <div class="space-y-5">
            <p class="text-sm font-semibold leading-none">Security preferences</p>

            <SecuritySwitchItem
              id="2-step-authentication"
              title="Enable 2-step authentication"
              description="Protects you against password theft by requesting an authentication code via SMS on every login." />

            <SecuritySwitchItem
              id="ask-change-password"
              title="Ask to change password on every 6 months"
              description="A simple but an effective way to be protected against data leaks and password theft." />
          </div>
        </div>

        <Button class="px-8 mt-8">Save</Button>
      </form>
    </CardContent>
  </Card>
</template>
