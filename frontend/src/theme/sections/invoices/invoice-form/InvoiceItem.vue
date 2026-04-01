<script lang="ts" setup>
import { watch } from "vue";
import { useFieldArray } from "vee-validate";
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { TableCell, TableRow } from "@/theme/components/ui/table";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
import TextField from "@/theme/components/form/TextField.vue";
// TYPES
import { InvoiceItem } from "./types";

const { fields, update, remove } = useFieldArray<InvoiceItem>("products");

const props = defineProps<{ id: number }>();

watch(
  () => fields.value[props.id],
  (current) => {
    if (!current.value || !current.value.quantity || !current.value.price) return;

    const { discount, price, quantity } = current.value;
    const subtotal = quantity * price;
    update(props.id, { ...current.value, total: subtotal - (discount || 0) });
  },
  { deep: true }
);
</script>

<template>
  <TableRow>
    <TableCell class="pl-1">
      <TextField
        :id="`products[${id}].title`"
        :name="`products[${id}].title`"
        placeholder="Ex: Product Title" />
    </TableCell>

    <TableCell>
      <TextField
        type="number"
        placeholder="Ex: 1"
        :id="`products[${id}].quantity`"
        :name="`products[${id}].quantity`" />
    </TableCell>

    <TableCell>
      <TextField
        type="number"
        placeholder="Ex: 100"
        :id="`products[${id}].price`"
        :name="`products[${id}].price`" />
    </TableCell>

    <TableCell>
      <TextField
        type="number"
        placeholder="Ex: 4"
        :id="`products[${id}].discount`"
        :name="`products[${id}].discount`" />
    </TableCell>

    <TableCell>
      <TextField
        :isDisable="true"
        placeholder="Ex: 55"
        :id="`products[${id}].total`"
        :name="`products[${id}].total`" />
    </TableCell>

    <TableCell class="pr-0">
      <Button size="sm" color="error" type="button" variant="outline" @click="remove(id)">
        <Icon name="Trash" :size="18" :strokeWidth="2" />
      </Button>
    </TableCell>
  </TableRow>
</template>
