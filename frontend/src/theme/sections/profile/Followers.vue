<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// DATA LIST
import { followers } from "@/theme/data/profile/followers";
</script>

<template>
  <Card class="p-6 xl:p-8">
    <CardTitle class="mb-6">Followers</CardTitle>

    <CardContent>
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div v-for="item in followers" :key="item.id">
          <RouterLink to="#">
            <Avatar shape="square" size="base" class="h-14 w-14 2xl:w-[72px] 2xl:h-[72px]">
              <AvatarImage :src="item.profileImage" alt="Profile Picture" />
              <AvatarFallback>P</AvatarFallback>
            </Avatar>
          </RouterLink>
        </div>
      </div>

      <Button variant="link" class="mt-6">See all followers</Button>
    </CardContent>
  </Card>
</template>
