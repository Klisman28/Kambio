<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENT
import UserForm from "@/theme/sections/users/UserForm.vue";
</script>

<template>
  <Card class="max-w-(--breakpoint-xl) p-6 mx-auto mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Create User</CardTitle>
    <UserForm />
  </Card>
</template>
