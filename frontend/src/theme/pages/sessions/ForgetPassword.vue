<script setup lang="ts">
import { Button } from "@/components/ui/button";
// CUSTOM COMPONENTS
import TextField from "@/components/form/TextField.vue";
</script>

<template>
  <div class="grid min-h-screen lg:grid-cols-2 bg-primary">
    <div class="hidden items-center px-20 py-20 text-white lg:flex xl:px-40">
      <div>
        <img src="/logos/uko.png" class="mb-10 h-10" alt="Uko" />
        <h4 class="mb-7 text-4xl font-bold">Hi, Welcome Back!</h4>
        <div>
          <h5 class="text-xl font-semibold">You are in a good company</h5>
          <p class="mt-2 text-sm leading-relaxed">
            Unlock the potential of Uko, where developers craft meticulously structured, visually
            stunning dashboards with feature-rich modules. Join us today to shape the future of your
            application development.
          </p>
        </div>
      </div>
    </div>

    <div
      class="content-center col-span-full p-10 sm:px-16 sm:py-20 bg-background lg:rounded-tl-[2rem] lg:rounded-bl-[2rem] md:px-40 lg:px-20 2xl:px-52 lg:col-span-1">
      <h3 class="font-semibold">Forgot Password?</h3>
      <p class="mt-1 mb-8 text-sm font-medium text-muted">Reset your Uko password</p>

      <p class="p-3 mb-4 text-sm text-center rounded-lg text-primary bg-primary/10">
        Provide your email address, and instructions will be sent to you
      </p>

      <form class="mt-8 space-y-6">
        <TextField id="email" name="email" label="Email" placeholder="Enter email" />

        <Button type="submit" class="w-full">Send Reset Link</Button>
      </form>
    </div>
  </div>
</template>
