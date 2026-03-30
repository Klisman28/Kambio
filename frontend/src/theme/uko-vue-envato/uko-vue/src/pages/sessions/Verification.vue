<script setup lang="ts">
import Button from "@/components/ui/button/Button.vue";
</script>

<template>
  <div class="grid min-h-screen lg:grid-cols-2 bg-primary">
    <div class="hidden items-center p-20 text-white lg:flex xl:px-40">
      <div class="space-y-4">
        <img src="/logos/uko.png" class="mb-10 h-10" alt="Uko" />

        <h4 class="mb-7 text-4xl font-bold">
          Welcome to <br />
          our community
        </h4>

        <p class="text-sm">
          Fuse helps developers to build organized and well coded dashboards full of beautiful and
          rich modules. Join us and start building your application today.
        </p>
      </div>
    </div>

    <div
      class="content-center col-span-full p-10 sm:px-16 sm:py-20 bg-background lg:rounded-tl-[2rem] lg:rounded-bl-[2rem] md:px-40 lg:px-20 2xl:px-52 lg:col-span-1">
      <img
        src="/images/illustration/emailVarification.svg"
        class="mb-4 w-20"
        alt="User Verification" />

      <h3 class="mb-1 font-semibold">Confirmation required</h3>
      <p class="text-sm text-muted">
        A confirmation mail with instructions has been sent to your email address. Follow those
        instructions to confirm your email address and activate your account.
      </p>

      <div class="flex flex-wrap gap-1 items-center mt-8">
        <p class="text-sm font-medium">Did you not receive an email?</p>
        <Button variant="link"> Please try again </Button>
      </div>
    </div>
  </div>
</template>
