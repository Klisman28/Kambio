<script setup lang="ts">
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
</script>

<template>
  <Card
    class="relative py-4 pl-5 col-span-full gradient-bg-2 2xl:col-span-4 xl:col-span-5 rtl:pr-5 rtl:pl-0">
    <div class="flex items-center h-full">
      <div>
        <h3 class="mb-3 text-lg font-semibold">
          Upgrade to <span class="text-primary">PRO</span> for <br />
          more resources
        </h3>

        <Button class="w-[135px] h-[38px] gradient-bg-1 text-xs font-semibold">Upgrade Now</Button>
      </div>
    </div>

    <img
      src="/images/illustration/Frame-1.png"
      class="absolute bottom-0 right-0 rtl:left-0 rtl:right-auto"
      alt="Illustration" />
  </Card>
</template>
