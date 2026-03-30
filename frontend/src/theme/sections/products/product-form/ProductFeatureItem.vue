<script lang="ts" setup>
import { useFieldArray } from "vee-validate";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import TextField from "@/components/form/TextField.vue";

defineProps<{ id: number }>();
const { remove } = useFieldArray("features");
</script>

<template>
  <div class="flex-1">
    <TextField
      :id="`features[${id}].name`"
      :name="`features[${id}].name`"
      placeholder="Ex: Feature name" />
  </div>

  <div class="flex-1">
    <TextField
      :id="`features[${id}].value`"
      :name="`features[${id}].value`"
      placeholder="Ex: Feature value" />
  </div>

  <div class="px-2">
    <button class="text-error" @click="remove(id)">
      <Icon name="Trash" :size="20" :strokeWidth="2" />
    </button>
  </div>
</template>
