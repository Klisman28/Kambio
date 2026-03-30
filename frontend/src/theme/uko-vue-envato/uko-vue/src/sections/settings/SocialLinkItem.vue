<script setup lang="ts">
import { Button } from "@/components/ui/button";
import Icon from "@/components/Icon.vue";

defineProps<{ icon: string; name: string; isConnected?: boolean; url?: string }>();
</script>

<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="grid w-8 h-8 p-1 text-white rounded-lg place-items-center bg-primary">
        <Icon :name="icon" :size="20" :strokeWidth="2" />
      </div>

      <div>
        <p class="text-sm font-semibold">{{ name }}</p>
        <p class="text-xs text-muted">
          {{ isConnected ? url : "Not connected" }}
        </p>
      </div>
    </div>

    <Button size="sm" variant="outline" v-if="isConnected">
      <Icon name="Check" :size="18" :stroke-width="2" />
      <span class="hidden ms-2 sm:inline">Connected</span>
    </Button>

    <Button size="sm" variant="outline" v-else>
      <Icon name="UserPlus" :size="18" :strokeWidth="2" />
      <span class="hidden ms-2 sm:inline">Connect</span>
    </Button>
  </div>
</template>
