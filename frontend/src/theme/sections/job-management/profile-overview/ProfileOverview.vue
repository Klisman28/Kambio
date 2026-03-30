<script setup lang="ts">
// SHADCN COMPONENTS
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import JobPostItem from "./JobPostItem.vue";
// CUSTOM DATA
import { recentJobPosts } from "@/data/dashboards/job-management";
</script>

<template>
  <Card class="p-6 col-span-full 2xl:col-span-4 xl:col-span-4">
    <CardContent>
      <div class="flex flex-col items-center gap-2">
        <Avatar size="base">
          <AvatarImage src="/images/users/07.jpg" alt="User" />
          <AvatarFallback>Av</AvatarFallback>
        </Avatar>

        <Badge class="px-[13px] py-[2px] font-medium text-[10px] mt-1">Pro</Badge>
        <p class="text-sm font-semibold">Neelesh Chaudhary</p>
        <p class="font-medium text-[12px] text-muted">UI / UX Designer</p>
        <p class="flex items-center gap-1 text-primary">
          <Icon name="MapPin" :size="20" />
          New York, US
        </p>
      </div>

      <!-- Recent Job -->
      <div class="mt-8">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-sm font-semibold">Recent Job Posted</h4>
          <Button variant="link">View all</Button>
        </div>

        <JobPostItem
          v-for="item in recentJobPosts"
          :key="item.id"
          :title="item.title"
          :value="item.number"
          :description="item.description" />

        <div class="flex justify-between w-full gap-4 mt-6">
          <Button size="lg" variant="outline" class="grow">Message</Button>
          <Button size="lg" class="grow">Connect</Button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
