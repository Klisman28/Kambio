<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
// DATA LIST
import galleries from "@/theme/data/profile/galleries";
</script>

<template>
  <Card class="p-6 xl:p-8">
    <CardTitle class="mb-6">Gallery</CardTitle>

    <CardContent>
      <div class="space-y-3">
        <div class="flex flex-wrap gap-4 justify-between grow">
          <img
            v-for="item in galleries"
            :key="item.id"
            :src="item.image"
            class="object-cover object-center w-14 h-10 rounded-sm 2xl:w-20 xl:h-16"
            alt="Gallery Image" />
        </div>
      </div>

      <Button variant="link" class="mt-6">See entire gallery</Button>
    </CardContent>
  </Card>
</template>
