<script setup lang="ts">
import { Card, CardContent } from "@/components/ui/card";
</script>

<template>
  <div class="px-4 py-10">
    <Card class="container mx-auto overflow-hidden bg-blue-950 rounded-2xl dark:bg-primary-light">
      <CardContent>
        <div class="lg:grid lg:grid-cols-2">
          <div class="px-12 py-10 space-y-5">
            <h3 class="text-2xl font-bold text-white lg:text-3xl text-balance">
              Haven't found an answer <br />
              to your question?
            </h3>

            <p class="text-base text-muted">
              Please comment below our product <br />
              and we will get back to you.
            </p>
          </div>

          <div class="inline-flex self-end justify-end">
            <img
              src="/images/illustration/Illustration-2.svg"
              alt="Contact"
              class="hidden w-3/4 lg:block" />
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
