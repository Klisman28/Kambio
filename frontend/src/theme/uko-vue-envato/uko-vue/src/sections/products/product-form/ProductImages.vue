<script setup lang="ts">
import { ErrorMessage, useField } from "vee-validate";
import { FileRejectReason, useDropzone } from "vue3-dropzone";
import Icon from "@/components/Icon.vue";
import { Label } from "@/components/ui/label";

const { value, errorMessage, setValue, setErrors } = useField<any>("images");

function onDrop(files: File[] | null, rejectReasons: FileRejectReason[]) {
  if (rejectReasons.length) {
    const { errors } = rejectReasons[0];
    if (errors.length) {
      const hasError: any = errors[0];
      setErrors(hasError.message);
    }
    return;
  }

  if (files) {
    const newFiles = files.map((file) => {
      return Object.assign(file, { preview: URL.createObjectURL(file) });
    });

    setValue(newFiles);
  }
}

const { getRootProps, getInputProps } = useDropzone({
  onDrop,
  multiple: true,
  maxSize: 3 * 1024 * 1024,
  accept: ["image/jpeg", "image/png", "image/gif", "image/jpg"]
});

const handleDelete = (index: number) => {
  const newImages = [...value.value];
  newImages.splice(index, 1);
  setValue(newImages);
};
</script>

<template>
  <div class="col-span-full">
    <Label for="images" class="inline-block mb-3 text-sm font-medium">Images</Label>

    <div
      v-bind="getRootProps()"
      class="relative flex flex-col items-center justify-center py-12 border border-dashed rounded-lg outline-hidden cursor-pointer border-border bg-slate-100/30 dark:bg-slate-700/10"
      :class="{ 'bg-red-100/20 border-error': errorMessage }">
      <Icon name="Image" :size="37" class="text-muted" />
      <p class="mt-4 text-xs text-muted">Drop your images here or</p>
      <p class="text-sm font-medium" :class="errorMessage ? 'text-error' : 'text-primary'">
        Select click to browse
      </p>

      <input class="hidden" v-bind="getInputProps()" />
    </div>

    <ErrorMessage name="images" class="block mt-3 ml-3 text-xs text-error" />

    <div class="inline-flex gap-4 mt-4" v-if="value?.length">
      <div class="relative overflow-hidden" v-for="(file, index) in value" :key="index">
        <img
          alt="product"
          :src="typeof file === 'string' ? file : file.preview"
          class="object-cover w-16 h-16 rounded-lg" />

        <button
          type="button"
          @click="handleDelete(index)"
          class="absolute p-0.5 rounded-lg top-1 right-1 bg-error/10">
          <Icon name="X" :size="14" :strokeWidth="2" class="text-error" />
        </button>
      </div>
    </div>
  </div>
</template>
