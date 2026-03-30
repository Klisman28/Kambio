<script setup lang="ts">
import { RouterLink, useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { push } from "notivue";
import * as yup from "yup";
// SHADCN COMPONENTS
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
// CUSTOM COMPONENTS
import Icon from "@/components/Icon.vue";
import TextField from "@/components/form/TextField.vue";
// AUTH COMPOSABLE
import { useAuth } from "@/auth/useAuth";

const router = useRouter();
const { register } = useAuth();

const validationSchema = yup.object({
  name: yup.string().required("Name is required"),
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup
    .string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),
  confirmPassword: yup
    .string()
    .min(6, "Password must be at least 6 characters")
    .test("passwordMatch", "Password do not match", function (value) {
      return this.parent.password === value;
    })
});

const { values, handleSubmit, isSubmitting, setFieldValue } = useForm({
  initialValues: { name: "", email: "", password: "", confirmPassword: "", terms: false },
  validationSchema
});

const onSubmit = handleSubmit(async (values) => {
  try {
    await register({
      name: values.name,
      email: values.email,
      password: values.password
    });

    router.replace({ name: "Dashboards" });
    push.success("User registered successfully");
  } catch (error) {
    push.error("Invalid credentials");
  }
});
</script>

<template>
  <div class="grid min-h-screen lg:grid-cols-2 bg-primary">
    <div class="hidden items-center px-20 py-20 text-white lg:flex xl:px-40">
      <div>
        <img src="/logos/uko.png" class="mb-10 h-10" alt="Uko" />
        <h4 class="mb-7 text-4xl font-bold">Hi, Welcome Back!</h4>
        <h5 class="text-xl font-semibold">You are in a good company</h5>
        <p class="mt-2 text-sm leading-relaxed">
          Unlock the potential of Uko, where developers craft meticulously structured, visually
          stunning dashboards with feature-rich modules. Join us today to shape the future of your
          application development.
        </p>
      </div>
    </div>

    <div
      class="content-center col-span-full p-10 sm:px-16 sm:py-20 bg-background lg:rounded-tl-[2rem] lg:rounded-bl-[2rem] md:px-40 lg:px-20 2xl:px-52 lg:col-span-1 lg:rtl:rounded-tr-[2rem] lg:rtl:rounded-br-[2rem] rtl:rounded-tl-none rtl:rounded-bl-none">
      <h3 class="font-semibold text-main">Sign Up</h3>
      <div class="flex gap-1 mt-1 mb-10 text-sm font-medium">
        <p class="text-muted">Already have an account?</p>
        <RouterLink to="/login" class="underline text-primary underline-offset-2">
          Login
        </RouterLink>
      </div>

      <form @submit="onSubmit">
        <div class="space-y-5">
          <TextField id="name" name="name" label="Name" placeholder="Enter name" />
          <TextField id="email" name="email" label="Email" placeholder="Enter email" />
          <TextField id="password" name="password" label="Password" placeholder="Enter password" />
          <TextField
            id="confirmPassword"
            name="confirmPassword"
            label="Confirm Password"
            placeholder="Enter password" />
        </div>

        <div class="flex gap-2 items-center mt-4">
          <Checkbox
            id="terms"
            class="w-4 h-4 rounded-sm border"
            :defaultChecked="values.terms"
            :onUpdate:checked="(value) => setFieldValue('terms', value)" />
          <label for="terms" class="text-[13px] font-medium leading-none">
            By registering you agree to the Uko
          </label>
        </div>

        <Button :disabled="isSubmitting" type="submit" class="mt-8! w-full">Sign Up</Button>
      </form>

      <div class="flex gap-2 justify-between items-center py-8 w-full">
        <hr class="grow border-border" />
        <p class="text-xs font-medium text-muted">OR</p>
        <hr class="grow border-border" />
      </div>

      <div class="flex gap-4 justify-center">
        <Button variant="outline" size="sm">
          <Icon name="Facebook" :size="20" :strokeWidth="0" class="fill-primary" />
        </Button>

        <Button variant="outline" size="sm">
          <Icon name="Linkedin" :size="20" :strokeWidth="0" class="fill-primary" />
        </Button>

        <Button variant="outline" size="sm">
          <Icon name="Twitter" :size="20" :strokeWidth="0" class="fill-primary" />
        </Button>
      </div>
    </div>
  </div>
</template>
