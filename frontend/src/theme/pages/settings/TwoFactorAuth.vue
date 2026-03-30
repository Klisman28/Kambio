<script setup lang="ts">
// SHADCN COMPONENTS
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle>Two-Factor Authentication (2FA) </CardTitle>
    <p class="mt-2 text-sm">
      Enhance your account security by enabling Two-Factor Authentication in the settings.
    </p>

    <CardContent>
      <form class="mt-6">
        <div>
          <Label for="ac-password">Account Password</Label>
          <p class="text-xs text-muted">Enter your current password to verify your identity.</p>
        </div>

        <div class="mt-3">
          <Input
            type="ac-password"
            id="ac-password"
            name="Account Password"
            placeholder="Account Password" />
          <p class="pt-1 text-xs text-muted">
            This is the password you use to log in to your account.
          </p>
        </div>

        <Button class="px-8 mt-6">Save Changes</Button>
      </form>
    </CardContent>
  </Card>
</template>
