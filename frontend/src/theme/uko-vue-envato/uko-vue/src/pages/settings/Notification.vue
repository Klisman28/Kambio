<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENTS
import ActivityItem from "@/sections/settings/ActivityItem.vue";
import SecuritySwitchItem from "@/sections/settings/SecuritySwitchItem.vue";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle class="mb-6 text-base leading-none">Notifications</CardTitle>

    <CardContent>
      <div class="space-y-5">
        <form class="space-y-8">
          <div class="space-y-4">
            <p class="text-sm font-medium">Security preferences</p>

            <SecuritySwitchItem
              id="communication"
              title="Communication"
              description="Get news, announcements, and product updates." />

            <SecuritySwitchItem
              id="security"
              title="Security"
              description="Get important notifications about your account security." />

            <SecuritySwitchItem
              id="meetups"
              title="Meetups"
              description="Get an email when a Meetup is posted close to my location." />
          </div>

          <!-- Account Activity -->
          <div class="space-y-4">
            <p class="text-sm font-medium">Account Activity</p>

            <div class="border divide-y rounded-lg divide-border border-border">
              <ActivityItem label="Someone comments on one of my items" id="comments" />
              <ActivityItem label="Someone mentions me" id="mentions-me" />
              <ActivityItem label="Someone follows me" id="follows-me" />
              <ActivityItem label="Someone replies to my job posting" id="replies-job-posting" />
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
