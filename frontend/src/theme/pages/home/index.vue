<script setup lang="ts">
import Header from "@/theme/sections/home/Header.vue";
import Banner from "@/theme/sections/home/Banner.vue";
import Contact from "@/theme/sections/home/Contact.vue";
import DemoTemplates from "@/theme/sections/home/DemoTemplates.vue";
import Features from "@/theme/sections/home/features/Features.vue";
</script>

<template>
  <Header></Header>
  <Banner />

  <main>
    <DemoTemplates />
    <Features />
    <Contact />
  </main>
</template>
