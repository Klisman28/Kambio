<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/components/ui/card";
// CUSTOM COMPONENT
import UserForm from "@/sections/users/UserForm.vue";
import { UserFormSkeleton } from "@/sections/users/skeletons";
// TYPES
import { User } from "@/types/User";

const route = useRoute();
const router = useRouter();

const user = ref<User>();
const error = ref();
const isLoading = ref(false);

const getUser = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<User>("/api/users", {
      params: { id: +route.params.id }
    });

    if (data) user.value = data;
    else router.push({ name: "NotFound" });
  } catch (err) {
    error.value = "Something went wrong";
  } finally {
    isLoading.value = false;
  }
};

onMounted(getUser);
</script>

<template>
  <Card class="max-w-(--breakpoint-xl) p-6 mx-auto mt-2 mb-6">
    <CardTitle class="mb-6 text-base">Edit User</CardTitle>
    <!-- SHOW LOADING SKELETON -->
    <UserFormSkeleton v-if="isLoading" />

    <!-- USER FORM WITH DATA -->
    <UserForm v-if="!isLoading && user" :user="user" />
  </Card>
</template>
