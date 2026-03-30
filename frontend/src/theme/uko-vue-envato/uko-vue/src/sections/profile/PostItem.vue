<script setup lang="ts">
// SHADCN COMPONENTS
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent
} from "@/components/ui/menubar";
import { Button } from "@/components/ui/button";
import { Card, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import AvatarGroup from "@/components/AvatarGroup.vue";
// TYPES
import { Post } from "@/types/Post";

defineProps<{ post: Post }>();
</script>

<template>
  <Card class="px-5 py-6 xl:p-8">
    <CardTitle class="flex justify-between mb-6">
      <div class="flex gap-4 items-center">
        <Avatar>
          <AvatarImage :src="post.user.image" :alt="post.user.name" />
          <AvatarFallback>{{ post.user.name }}</AvatarFallback>
        </Avatar>

        <div>
          <p class="text-sm">{{ post.user.name }}</p>
          <p class="text-xs font-normal text-muted">{{ post.createdAt }} minutes ago</p>
        </div>
      </div>

      <Menubar class="p-0 -mt-2 bg-transparent">
        <MenubarMenu>
          <MenubarTrigger
            class="inline-flex justify-center p-1 w-6 h-6 text-lg rounded-sm text-slate-500 bg-slate-100 dark:bg-slate-700 dark:text-slate-400 dark:hover:text-slate-100">
            <Icon name="Ellipsis" :size="18" class="" />
          </MenubarTrigger>

          <MenubarContent align="end" class="">
            <MenubarItem class="gap-2 px-4 py-2 font-medium text-card-foreground">
              <Icon name="Eye" :size="18" /> Save post
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="EyeOff" :size="18" /> Hide post
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="EyeOff" :size="18" /> Hide all
            </MenubarItem>

            <hr class="my-2 dark:border-slate-600" />

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="BadgeAlert" :size="18" /> Report post
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="Bell" :size="18" /> Turn on notifications
            </MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
    </CardTitle>

    <div class="space-y-5">
      <p class="text-sm">{{ post.content }}</p>

      <img
        v-if="post.thumbnail"
        :src="post.thumbnail"
        :alt="post.content"
        class="object-cover object-center w-full h-full rounded-md" />

      <div class="flex gap-4">
        <Button class="px-4 text-primary! rounded-full bg-transparent hover:bg-primary/10">
          <Icon :size="18" name="Heart" class="hidden sm:inline sm:me-1.5" />
          <span>Unlike</span>
        </Button>

        <Button class="px-4 text-primary! rounded-full bg-transparent hover:bg-primary/10">
          <Icon name="MessageSquare" :size="18" class="hidden sm:inline sm:me-1.5" />
          <span>Comment</span>
        </Button>

        <Button class="px-4 text-primary! rounded-full bg-transparent hover:bg-primary/10">
          <Icon name="Share2" :size="18" class="hidden sm:inline sm:me-1.5" />
          <span>Share</span>
        </Button>
      </div>
    </div>

    <hr class="my-6 border-border" />

    <div class="flex gap-2 justify-between items-center">
      <div class="flex gap-3 items-center">
        <AvatarGroup
          size="xs"
          :images="[
            '/images/users/01.jpg',
            '/images/users/02.jpg',
            '/images/users/03.jpg',
            '/images/users/02.jpg'
          ]" />
        <p class="text-sm font-normal leading-none truncate text-muted">
          you and {{ post.totalLikes }} more liked this
        </p>
      </div>

      <div class="hidden gap-4 items-center sm:flex">
        <Button class="px-4 text-primary! rounded-full bg-transparent hover:bg-primary/10">
          {{ post.totalShares }} shares
        </Button>

        <Button class="px-4 text-primary! rounded-full bg-transparent hover:bg-primary/10">
          <Icon name="ChevronDown" :size="18" class="me-1.5 group-hover:text-primary" />
          {{ post.totalComments }} Comments
        </Button>
      </div>
    </div>
  </Card>
</template>
