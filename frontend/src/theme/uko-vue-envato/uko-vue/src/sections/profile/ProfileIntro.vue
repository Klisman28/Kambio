<script setup lang="ts">
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
</script>

<template>
  <div class="mb-6">
    <div class="h-40 overflow-hidden rounded-t-lg lg:h-80">
      <img
        alt="cover-image"
        src="/images/covers/cover-1.jpg"
        class="object-cover object-center w-full" />
    </div>

    <Card class="p-5 rounded-tl-none rounded-tr-none border-t-none">
      <CardContent class="mx-auto xl:w-11/12">
        <div class="flex flex-col items-center justify-between gap-4 xl:flex-row">
          <div class="flex flex-col justify-center gap-3 text-center xl:text-left xl:flex-row">
            <Avatar size="lg" class="-mt-20 border-2 border-white">
              <AvatarImage src="/images/users/01.jpg" alt="Profile Image" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>

            <div class="flex flex-col items-center justify-center gap-4 xl:flex-row">
              <div class="px-4 mx-4 xl:px-8 xl:mx-8 xl:border-e dark:border-e-gray-600">
                <h5 class="text-base font-semibold">Brian Huges</h5>
                <p class="text-muted">London, UK</p>
              </div>

              <div class="flex flex-wrap gap-4 lg:gap-8">
                <div>
                  <h5 class="text-base font-semibold">200k</h5>
                  <p class="text-xs text-muted">FOLLOWERS</p>
                </div>

                <div>
                  <h5 class="text-base font-semibold">1.2k</h5>
                  <p class="text-xs text-muted">FOLLOWING</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap gap-6 text-center">
            <RouterLink
              to="#"
              class="p-2 text-sm font-medium transition duration-300 text-primary hover:text-primary">
              Home
            </RouterLink>
            <RouterLink
              to="#"
              class="p-2 text-sm font-medium transition duration-300 text-muted hover:text-primary">
              About
            </RouterLink>
            <RouterLink
              to="#"
              class="p-2 text-sm font-medium transition duration-300 text-muted hover:text-primary">
              Followers
            </RouterLink>
            <RouterLink
              to="#"
              class="p-2 text-sm font-medium transition duration-300text-muted hover:text-primary">
              Gallery
            </RouterLink>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
