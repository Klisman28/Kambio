<script setup lang="ts">
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import * as yup from "yup";
// SHADCN COMPONENTS
import { Button } from "@/theme/components/ui/button";
import { SelectItem } from "@/theme/components/ui/select";
// CUSTOM COMPONENTS
import UserImageUpload from "./UserImageUpload.vue";
import TextField from "@/theme/components/form/TextField.vue";
import SelectField from "@/theme/components/form/SelectField.vue";
// USER STORE
import { useUsers } from "@/theme/stores/users";
// TYPES
import { User } from "@/theme/types/User";

const { user } = defineProps<{ user?: User }>();

const router = useRouter();
const { createNewUser, updateUser } = useUsers();

const validationSchema = yup.object({
  name: yup.string().required("Name is required"),
  role: yup.string().required("Role is required"),
  status: yup.string().required("Status is required"),
  address: yup.string().required("Address is required"),
  phone: yup.string().required("Phone is required"),
  image: yup.mixed().nullable().required("Image is required"),
  email: yup.string().required("Email is required").email("Invalid email")
});

const { handleSubmit, isSubmitting } = useForm({
  validationSchema,
  initialValues: {
    name: user?.name || "",
    role: user?.role || "",
    email: user?.email || "",
    phone: user?.phone || "",
    image: user?.image || null,
    status: user?.status || "",
    address: user?.address || ""
  }
});

// FORM SUBMIT HANDLER
const onSubmit = handleSubmit((values, { resetForm }) => {
  const payload = {
    name: values.name,
    role: values.role,
    email: values.email,
    phone: values.phone,
    image: values.image!,
    status: values.status,
    address: values.address
  };

  if (user) {
    updateUser(user.id, payload);
    router.push({ name: "Users" });
    return;
  }

  createNewUser(payload);
  resetForm();
});
</script>

<template>
  <form @submit="onSubmit">
    <div class="grid grid-cols-12 gap-7">
      <div class="flex flex-col items-center justify-center col-span-full lg:col-span-4">
        <UserImageUpload />
      </div>

      <div
        class="mb-10 space-y-4 col-span-full lg:col-span-8 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-7">
        <TextField id="name" name="name" label="User Name" placeholder="John Doe" />

        <TextField
          id="email"
          type="email"
          name="email"
          label="Email"
          placeholder="example@domain.com" />

        <TextField id="phone" name="phone" label="Phone Number" placeholder="0123456789" />

        <SelectField id="status" name="status" label="Status" placeholder="Select a status">
          <SelectItem value="Hidden">Hidden</SelectItem>
          <SelectItem value="Rejected">Rejected</SelectItem>
          <SelectItem value="Verified">Verified</SelectItem>
          <SelectItem value="Waiting">Waiting</SelectItem>
        </SelectField>

        <TextField id="role" name="role" label="Role" placeholder="Web Developer" />
        <TextField id="address" name="address" label="Address" placeholder="New York, USA" />
      </div>
    </div>

    <Button type="submit" :disabled="isSubmitting" class="block ms-auto">
      {{ user ? "Update User" : "Create User" }}
    </Button>
  </form>
</template>
