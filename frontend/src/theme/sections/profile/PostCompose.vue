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
import { Textarea } from "@/components/ui/textarea";
import { Card, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
</script>

<template>
  <Card class="p-6 space-y-8 xl:p-8">
    <CardTitle class="mb-4">Create Post</CardTitle>

    <div class="flex gap-4">
      <Avatar class="hidden sm:block">
        <AvatarImage src="/images/users/01.jpg" alt="@radix-vue" />
        <AvatarFallback>CN</AvatarFallback>
      </Avatar>

      <Textarea rows="6" placeholder="What's on your mind?"></Textarea>
    </div>

    <div class="hidden gap-2 sm:flex 2xl:gap-3">
      <Button
        class="px-3 text-primary! text-medium rounded-full bg-transparent hover:bg-primary/10">
        <Icon name="Image" :size="20" class="me-1" /> Photo / Video
      </Button>

      <Button
        class="px-3 text-primary! text-medium rounded-full bg-transparent hover:bg-primary/10">
        <Icon name="User" :size="20" class="me-1" /> Tag Friends
      </Button>

      <div class="hidden xl:block">
        <Button
          class="px-3 text-primary! text-medium rounded-full bg-transparent hover:bg-primary/10">
          <Icon name="Smile" :size="20" class="me-1" /> Feeling
        </Button>
      </div>

      <Menubar class="bg-transparent">
        <MenubarMenu>
          <MenubarTrigger
            class="py-[10px] px-4 inline-flex text-primary bg-transparent hover:bg-primary/20 justify-center rounded-full text-lg hover:text-primary">
            <Icon name="Ellipsis" :size="18" />
          </MenubarTrigger>

          <MenubarContent align="end">
            <MenubarItem class="gap-2 px-4 py-2 font-medium xl:hidden text-card-foreground">
              <Icon name="Smile" :size="18" /> Feeling
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 font-medium text-card-foreground">
              <Icon name="Play" :size="18" /> Live
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="Sparkles" :size="18" /> Gif
            </MenubarItem>

            <MenubarItem class="gap-2 px-4 py-2 text-[13px] text-card-foreground font-medium">
              <Icon name="Map" :size="18" /> Check in
            </MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
    </div>
  </Card>
</template>
