<script setup lang="ts">
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
// CUSTOM COMPONENT
import TextField from "@/components/form/TextField.vue";
import ProfileWidget from "@/sections/settings/ProfileWidget.vue";
</script>

<template>
  <Card class="p-5 xl:p-6">
    <CardContent>
      <form class="space-y-10">
        <ProfileWidget title="Profile">
          <TextField id="name" name="name" label="Name" placeholder="Full Name" />
          <TextField id="username" name="username" label="Username" placeholder="Username" />

          <TextField
            id="designation"
            name="designation"
            label="Designation"
            placeholder="Designation" />

          <TextField id="company" name="company" label="Company Name" placeholder="Company" />

          <div class="col-span-full">
            <Label for="about" class="block mb-3">About</Label>
            <Textarea id="about" placeholder="About here."></Textarea>
          </div>
        </ProfileWidget>

        <ProfileWidget title="Personal Information">
          <TextField type="email" id="email" name="email" label="Email" placeholder="Email" />
          <TextField id="phone" name="phone" label="Phone Number" placeholder="Phone Number" />
          <TextField id="country" name="country" label="Country" placeholder="Country" />
          <TextField id="language" name="language" label="Language" placeholder="Language" />
        </ProfileWidget>

        <Button class="px-8">Save</Button>
      </form>
    </CardContent>
  </Card>
</template>
