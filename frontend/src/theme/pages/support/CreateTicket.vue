<script setup lang="ts">
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { Card, CardContent, CardTitle } from "@/theme/components/ui/card";
import { SelectItem } from "@/theme/components/ui/select";
// CUSTOM COMPONENTS
import TextField from "@/theme/components/form/TextField.vue";
import SelectField from "@/theme/components/form/SelectField.vue";
import TextAreaField from "@/theme/components/form/TextAreaField.vue";
</script>

<template>
  <Card class="p-6 xl:py-8 mt-7">
    <div class="max-w-(--breakpoint-lg) mx-auto">
      <CardTitle class="text-base">Create Ticket</CardTitle>
      <p class="text-muted font-normal text-sm mt-1 mb-6">
        Please include as many details as possible about your question or problem.
      </p>

      <CardContent>
        <div class="space-y-2">
          <p class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-muted"></span> Screenshots/Screen Recording is very
            helpful.
          </p>
          <p class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-muted"></span> You can use snipboard.io to share
            screenshots.
          </p>
          <p class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-muted"></span> And loom.com for screen recording.
          </p>
        </div>

        <form class="pt-10">
          <div class="grid grid-cols-12 gap-6">
            <div class="col-span-6">
              <TextField
                id="first-name"
                name="first-name"
                label="First Name"
                placeholder="First Name" />
            </div>

            <div class="col-span-6">
              <TextField
                id="last-name"
                name="last-name"
                label="Last Name"
                placeholder="Last Name" />
            </div>

            <div class="col-span-full">
              <TextField id="email" name="email" label="Email" placeholder="Email" />
            </div>

            <div class="col-span-full">
              <SelectField id="product" name="product" label="Product" placeholder="Select product">
                <SelectItem value="product-1"> Product-1 </SelectItem>
                <SelectItem value="product-2"> Product-2 </SelectItem>
                <SelectItem value="product-3"> Product-3 </SelectItem>
                <SelectItem value="product-4"> Product-4 </SelectItem>
              </SelectField>
            </div>

            <div class="col-span-full">
              <TextField id="subject" name="subject" label="Subject" placeholder="Subject" />
            </div>

            <div class="col-span-full">
              <TextAreaField
                id="message"
                name="message"
                label="Message"
                placeholder="Write your message" />
            </div>
          </div>

          <Button class="px-8 mt-8">Submit</Button>
        </form>
      </CardContent>
    </div>
  </Card>
</template>
