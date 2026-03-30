<script setup lang="ts">
import TextFieldSkeleton from "./TextFieldSkeleton.vue";
</script>

<template>
  <form>
    <div class="grid grid-cols-12 gap-7">
      <div class="flex flex-col items-center justify-center col-span-full lg:col-span-4">
        <div
          class="w-32 h-32 rounded-full bg-skeleton animate-pulse outline-border outline-offset-8 outline-dashed outline-1"></div>
      </div>

      <div
        class="mb-10 space-y-4 col-span-full lg:col-span-8 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-7">
        <TextFieldSkeleton label="User Name" />
        <TextFieldSkeleton label="Email" />
        <TextFieldSkeleton label="Status" />
        <TextFieldSkeleton label="Role" />
        <TextFieldSkeleton label="Address" />
      </div>
    </div>

    <div class="h-10 rounded-md w-28 bg-skeleton animate-pulse ms-auto"></div>
  </form>
</template>
