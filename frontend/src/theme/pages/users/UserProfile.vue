<script setup lang="ts">
import About from "@/theme/sections/profile/About.vue";
import Groups from "@/theme/sections/profile/Groups.vue";
import Gallery from "@/theme/sections/profile/Gallery.vue";
import PostList from "@/theme/sections/profile/PostList.vue";
import Followers from "@/theme/sections/profile/Followers.vue";
import PostCompose from "@/theme/sections/profile/PostCompose.vue";
import ProfileIntro from "@/theme/sections/profile/ProfileIntro.vue";
</script>

<template>
  <!-- USER PROFILE OVERVIEW -->
  <ProfileIntro />

  <div class="grid grid-cols-12 mb-6 gap-7">
    <div class="hidden col-span-5 space-y-6 xl:block 2xl:col-span-4">
      <About />
      <Followers />
      <Gallery />
      <Groups />
    </div>

    <div class="space-y-6 col-span-full 2xl:col-span-8 xl:col-span-7">
      <PostCompose />
      <PostList />
    </div>
  </div>
</template>
