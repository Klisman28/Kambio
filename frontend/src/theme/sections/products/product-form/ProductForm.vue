<script setup lang="ts">
import { useRouter } from "vue-router";
import { useFieldArray, useForm } from "vee-validate";
import * as yup from "yup";
// SHADCN COMPONENTS
import { Label } from "@/theme/components/ui/label";
import { Button } from "@/theme/components/ui/button";
import { Switch } from "@/theme/components/ui/switch";
// CUSTOM COMPONENTS
import Sizes from "./Sizes.vue";
import Colors from "./Colors.vue";
import Categories from "./Categories.vue";
import ProductImages from "./ProductImages.vue";
import ProductFeatureItem from "./ProductFeatureItem.vue";
import Icon from "@/theme/components/Icon.vue";
import TextField from "@/theme/components/form/TextField.vue";
import TextAreaField from "@/theme/components/form/TextAreaField.vue";
// STORE
import { useProducts } from "@/theme/stores/products";
// TYPE
import { Product } from "@/theme/types/Product";

const { product } = defineProps<{ product?: Product }>();
const { createNewProduct, updateProduct } = useProducts();
const router = useRouter();

const validationSchema = yup.object({
  title: yup.string().required("Product title is required"),
  category: yup.string().required("Category is required"),
  code: yup.string().required("Code is required"),
  price: yup.number().required("Price is required"),
  colors: yup
    .array()
    .of(yup.string())
    .min(1, "At least one size is required")
    .required("Color is required"),
  sizes: yup
    .array()
    .of(yup.string())
    .min(1, "At least one size is required")
    .required("Size is required"),
  description: yup.string().required("Description is required"),
  features: yup
    .array()
    .of(
      yup.object({
        name: yup.string().required("Name is required"),
        value: yup.string().required("Value is required")
      })
    )
    .required("Features is required"),
  stock: yup.number().required("Stock is required"),
  images: yup
    .array()
    .of(yup.mixed())
    .min(2, "Must have at least 2 images!")
    .required("Images is required")
});

const { values, isSubmitting, handleSubmit, setFieldValue } = useForm({
  validationSchema,
  initialValues: {
    title: product?.title || "",
    code: product?.code || "",
    category: product?.category || "",
    images: product?.images || [],
    price: product?.price || null,
    colors: product?.colors || [],
    sizes: product?.sizes || [],
    description: product?.description || "",
    features: product?.features || [{ name: "", value: "" }],
    stock: product?.stock || null,
    status: product?.status === "Published" || false
  }
});

// FORM FEATURES FIELD
const { fields, push } = useFieldArray("features");

// FORM SUBMIT HANDLER
const onSubmit = handleSubmit((values, { resetForm }) => {
  const images = values.images.map((image: any) =>
    typeof image === "string" ? image : image.preview
  );
  const payload = {
    images,
    code: values.code,
    title: values.title,
    price: values.price!,
    stock: values.stock!,
    sizes: values.sizes,
    colors: values.colors,
    status: values.status,
    category: values.category,
    features: values.features,
    description: values.description
  };

  if (product) {
    updateProduct(product.id, payload);
    router.push({ name: "Products" });
    return;
  }

  createNewProduct(payload);
  resetForm();
});
</script>

<template>
  <form @submit="onSubmit">
    <div class="space-y-6 md:space-y-0 md:grid md:grid-cols-2 md:gap-6">
      <div class="col-span-full">
        <TextField id="title" name="title" label="Title" placeholder="Product title" />
      </div>

      <TextField id="code" name="code" label="Code" placeholder="Product code" />

      <Categories />

      <TextField type="number" id="price" name="price" label="Price" placeholder="Product price" />

      <TextField
        type="number"
        id="stock"
        name="stock"
        label="Stock"
        placeholder="Product quantity" />

      <Colors />

      <Sizes />

      <ProductImages />

      <div class="col-span-full">
        <TextAreaField
          id="description"
          name="description"
          label="Description"
          placeholder="Ex: Product Description" />
      </div>

      <div class="col-span-full">
        <h4 class="mb-3 text-sm font-medium">Features</h4>

        <div class="space-y-5">
          <div :key="id" v-for="(_, id) in fields" class="flex items-center justify-between gap-8">
            <ProductFeatureItem :id="id" />
          </div>

          <Button size="sm" type="button" color="success" @click="push({ name: '', value: '' })">
            <Icon name="Plus" :size="18" :strokeWidth="2" class="me-1" /> Add
          </Button>
        </div>
      </div>

      <div class="flex flex-wrap justify-between gap-6 col-span-full">
        <div class="flex items-center gap-2">
          <Switch
            id="status"
            :checked="values.status"
            @update:checked="setFieldValue('status', $event)" />
          <Label for="status" class="text-sm font-medium">Publish</Label>
        </div>

        <Button type="submit" :disabled="isSubmitting">{{ product ? "Update" : "Create" }}</Button>
      </div>
    </div>
  </form>
</template>
