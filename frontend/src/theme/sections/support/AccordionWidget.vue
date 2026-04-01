<script setup lang="ts">
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent
} from "@/theme/components/ui/accordion";
import { Badge } from "@/theme/components/ui/badge";

// ==============================================================
interface Item {
  value: string;
  title: string;
  content: string;
  category?: string;
}
// ==============================================================

defineProps<{ list: Item[]; defaultValue?: string }>();
</script>

<template>
  <Accordion type="single" collapsible :default-value="defaultValue">
    <AccordionItem v-for="item in list" :key="item.value" :value="item.value">
      <AccordionTrigger>
        <div class="truncate">
          {{ item.title }}
          <Badge class="ms-1 hidden sm:inline-flex" v-if="item.category">{{ item.category }}</Badge>
        </div>
      </AccordionTrigger>

      <AccordionContent>{{ item.content }}</AccordionContent>
    </AccordionItem>
  </Accordion>
</template>
