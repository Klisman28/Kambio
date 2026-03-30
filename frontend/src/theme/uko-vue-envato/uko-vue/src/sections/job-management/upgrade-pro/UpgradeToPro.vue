<script setup lang="ts">
import { Card, CardTitle } from "@/components/ui/card";
</script>

<template>
  <Card
    class="flex flex-col justify-between gap-6 px-6 pt-6 col-span-full 2xl:col-span-4 xl:col-span-5 lg:col-span-5 md:gap-10">
    <CardTitle class="text-lg font-semibold text-center">
      Upgrade to <span class="text-primary">PRO</span> for <br />
      more resources
    </CardTitle>

    <div class="flex justify-end w-full px-8 md:w-2/3 md:mx-auto lg:w-full">
      <img src="/images/illustration/Illustration-1.svg" class="w-full" />
    </div>
  </Card>
</template>
