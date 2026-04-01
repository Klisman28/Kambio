<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
// DATA LIST
import groups from "@/theme/data/profile/groups";
</script>

<template>
  <Card class="p-6 xl:p-8">
    <CardTitle class="mb-6">Groups</CardTitle>

    <CardContent>
      <div class="space-y-4">
        <div class="flex gap-4 items-center" v-for="group in groups" :key="group.id">
          <img :src="group.groupImg" alt="Group Image" class="object-cover w-14 h-14 rounded-sm" />

          <div class="truncate">
            <p class="text-sm font-medium">{{ group.name }}</p>
            <p class="text-xs font-normal text-muted">
              {{ group.description }}
            </p>

            <p class="mt-1 text-muted">{{ group.followers }}k followers</p>
          </div>
        </div>
      </div>

      <Button variant="link" class="mt-6">See all groups</Button>
    </CardContent>
  </Card>
</template>
