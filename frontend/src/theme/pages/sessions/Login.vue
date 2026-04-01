<script setup lang="ts">
import { RouterLink, useRoute, useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { push } from "notivue";
import * as yup from "yup";
// SHADCN COMPONENTS
import { Checkbox } from "@/theme/components/ui/checkbox";
import { Button } from "@/theme/components/ui/button";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
import TextField from "@/theme/components/form/TextField.vue";
// AUTH COMPOSABLE
import { useAuth } from "@/theme/auth/useAuth";

const route = useRoute();
const router = useRouter();
const { login } = useAuth();

const validationSchema = yup.object({
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup
    .string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required")
});

const { values, handleSubmit, isSubmitting, setFieldValue } = useForm({
  validationSchema,
  initialValues: {
    email: "nabedkhan@gmail.com",
    password: "123456789",
    remember: true
  }
});

const onSubmit = handleSubmit(async (values) => {
  try {
    await login({ email: values.email, password: values.password, rememberMe: values.remember });
    const redirectTo = route.query.redirect?.toString() || "/dashboards";
    router.replace(redirectTo);
    push.success("User logged in successfully");
  } catch (error) {
    push.error("Invalid credentials");
  }
});
</script>

<template>
  <div class="grid min-h-screen lg:grid-cols-2 bg-primary">
    <div class="hidden items-center p-20 text-white lg:flex xl:px-40">
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
      <h3 class="font-semibold">Sign In</h3>
      <div class="flex gap-1 mt-1 mb-10 text-sm font-medium">
        <p class="text-muted">New user?</p>
        <RouterLink to="/register" class="underline text-primary underline-offset-2">
          Create an Account
        </RouterLink>
      </div>

      <form @submit="onSubmit">
        <div class="space-y-5">
          <TextField id="email" name="email" label="Email" placeholder="Enter email" />
          <TextField
            id="password"
            type="password"
            name="password"
            label="Password"
            placeholder="Enter password" />
        </div>

        <div class="flex justify-between mt-3">
          <div class="flex gap-2 items-center">
            <Checkbox
              id="remember"
              class="w-4 h-4 rounded-sm border"
              :defaultChecked="values.remember"
              :onUpdate:checked="(value) => setFieldValue('remember', value)" />
            <label for="remember" class="text-sm font-medium leading-none">Remember me</label>
          </div>

          <RouterLink
            to="/forget-password"
            class="text-sm transition-all text-primary hover:underline underline-offset-2">
            Forget Password?
          </RouterLink>
        </div>

        <Button :disabled="isSubmitting" type="submit" class="mt-8! w-full">Sign In</Button>
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
