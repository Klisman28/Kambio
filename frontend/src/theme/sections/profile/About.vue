<script setup lang="ts">
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
</script>

<template>
  <Card class="p-6 xl:p-8">
    <CardTitle class="mb-4">About Me</CardTitle>

    <CardContent class="space-y-6">
      <p class="text-sm font-normal text-muted">
        I’m a friendly kitchen assistant who suffers from a severe phobia of buttons. Brother of
        Elijah Jay Watkins, who has phobia of buttons and trust issues.
      </p>

      <hr class="border-border" />

      <div class="space-y-3">
        <p class="flex items-center gap-2">
          <Icon name="MapPin" :size="19" :strokeWidth="1.5" class="text-muted" />
          London, UK
        </p>

        <p class="flex items-center gap-2">
          <Icon name="Briefcase" :size="19" :strokeWidth="1.5" class="text-muted" />
          ACME Corp. Lead UX Designer
        </p>

        <p class="flex items-center gap-2">
          <Icon name="Gift" :size="19" :strokeWidth="1.5" class="text-muted" />
          April, 24
        </p>
      </div>

      <Button class="w-full">See complete bio</Button>
    </CardContent>
  </Card>
</template>
