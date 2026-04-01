<script setup lang="ts">
import { useField } from "vee-validate";
import { FileRejectReason, useDropzone } from "vue3-dropzone";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
import { cn } from "@/theme/lib/utils";

const { value, errorMessage, setValue, setErrors } = useField<any>("image");

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
    const file = files[0];
    const newFile = Object.assign(file, { preview: URL.createObjectURL(file) });
    setValue(newFile);
  }
}

const { getRootProps, getInputProps } = useDropzone({
  onDrop,
  maxFiles: 1,
  maxSize: 3 * 1024 * 1024,
  accept: ["image/jpeg", "image/png", "image/gif", "image/jpg"]
});
</script>

<template>
  <div
    v-bind="getRootProps()"
    :class="
      cn([
        'relative w-32 h-32 overflow-hidden transition-all duration-300 rounded-full bg-slate-100 cursor-pointer group outline-border outline-offset-8 outline-dashed outline-1 dark:bg-slate-900/10',
        {
          'hover:opacity-75': !value,
          'outline-error bg-red-200': errorMessage,
          'hover:after:content-[\'\'] hover:after:absolute hover:after:w-full hover:after:h-full hover:after:bg-slate-900/20 hover:after:inset-0 after:z-10':
            value
        }
      ])
    ">
    <img
      alt="User"
      v-if="value"
      :src="typeof value === 'string' ? value : value.preview"
      class="relative z-10 object-cover w-full h-full" />

    <div
      class="absolute inset-0 grid place-items-center text-slate-300"
      :class="{ 'group-hover:z-10 group-hover:text-white': value }">
      <input class="hidden" v-bind="getInputProps()" />
      <Icon :size="28" name="Camera" :strokeWidth="2" />
    </div>
  </div>

  <div class="max-w-56">
    <p class="mt-6 text-xs text-center text-muted">
      Allowed *.jpeg, *.jpg, *.png, <br />
      *.gif max size of 3 Mb
    </p>

    <p v-if="errorMessage" class="mt-2 text-xs text-center text-error">
      {{ errorMessage }}
    </p>
  </div>
</template>
