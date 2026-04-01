<script setup lang="ts">
import { Button } from "@/theme/components/ui/button";
import PostItem from "./PostItem.vue";
// DATA LIST
import posts from "@/theme/data/profile/posts";
</script>

<template>
  <PostItem v-for="post in posts" :key="post.id" :post="post" />

  <div class="pt-4 text-center">
    <Button>Load More</Button>
  </div>
</template>
