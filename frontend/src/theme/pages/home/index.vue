<script setup lang="ts">
import Header from "@/sections/home/Header.vue";
import Banner from "@/sections/home/Banner.vue";
import Contact from "@/sections/home/Contact.vue";
import DemoTemplates from "@/sections/home/DemoTemplates.vue";
import Features from "@/sections/home/features/Features.vue";
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
