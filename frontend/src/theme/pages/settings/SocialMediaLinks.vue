<script setup lang="ts">
// SHADCN COMPONENTS
import { Card, CardContent, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENTS
import SocialLinkItem from "@/sections/settings/SocialLinkItem.vue";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardTitle class="mb-6 text-base leading-none">Social Media Links</CardTitle>

    <CardContent>
      <div class="space-y-5">
        <SocialLinkItem icon="Linkedin" name="Linkedin" />
        <SocialLinkItem icon="Dribbble" name="Dribble" />
        <SocialLinkItem icon="Twitter" name="Twitter" :isConnected="true" url="#" />
        <SocialLinkItem icon="Facebook" name="Facebook" :isConnected="true" url="#" />
        <SocialLinkItem icon="Instagram" name="Instagram" />
      </div>
    </CardContent>
  </Card>
</template>
