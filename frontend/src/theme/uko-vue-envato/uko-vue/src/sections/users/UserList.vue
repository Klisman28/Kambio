<script setup lang="ts">
import { toRefs } from "vue";
import { RouterLink } from "vue-router";
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import {
  Table,
  TableRow,
  TableCell,
  TableBody,
  TableHead,
  TableHeader
} from "@/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarContent,
  MenubarTrigger
} from "@/components/ui/menubar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge, BadgeVariants } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
// CUSTOM COMPONENTS
import { UserListSkeleton } from "./skeletons";
import Icon from "@/components/Icon.vue";
import TablePagination from "@/components/TablePagination.vue";
// USER STORE
import { useUsers } from "@/stores/users";
// CUSTOM UTILS METHODS
import { dateFormat } from "@/lib/dateFormat";
import { formatPhoneNumber } from "@/lib/libPhoneNumber";

const { state, deleteUser, resetFilter } = useUsers();
const { filters, users, meta, isLoading } = toRefs(state);

const getBadgeVariant = (status: string): BadgeVariants["variant"] => {
  const str = status.toLowerCase();
  if (str === "verified") return "default";
  else if (str === "waiting") return "success";
  else if (str === "hidden") return "secondary";
  else if (str === "rejected") return "destructive";
};

const tableHeads = [
  "User ID",
  "Name",
  "Location",
  "Email",
  "Phone Number",
  "Joining Date",
  "Status",
  "Action"
];
</script>

<template>
  <Card class="mb-6">
    <!-- User Table -->
    <Scrollbar>
      <Table class="min-w-[1200px]">
        <TableHeader>
          <TableRow>
            <TableHead :key="head" v-for="head in tableHeads" class="py-5">{{ head }}</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <!-- LOADING SKELETON -->
          <template v-if="isLoading">
            <UserListSkeleton v-for="i in 10" :key="i" />
          </template>

          <!-- NOT FOUND USER MESSAGE -->
          <TableRow v-else-if="!isLoading && users.length === 0">
            <TableCell colspan="8" class="py-24 m-4 text-center bg-slate-200/20">
              <p class="mb-4 text-2xl">No users found for '{{ filters.search }}'</p>
              <Button variant="outline" class="rounded-full" @click="resetFilter()">
                Clear your search and try again
              </Button>
            </TableCell>
          </TableRow>

          <TableRow
            v-else
            :key="user.id"
            v-for="user in users"
            class="[&>td]:font-normal [&>td]:border-b [&>td]:border-border">
            <TableCell>{{ user.id }}</TableCell>
            <TableCell>
              <div class="flex gap-2 items-center">
                <Avatar shape="square">
                  <AvatarImage :src="user.image" alt="User" />
                  <AvatarFallback>U</AvatarFallback>
                </Avatar>

                <div>
                  <p class="font-medium">{{ user.name }}</p>
                  <span class="text-xs text-muted">
                    {{ user.role }}
                  </span>
                </div>
              </div>
            </TableCell>

            <TableCell>{{ user.address }}</TableCell>
            <TableCell>{{ user.email }}</TableCell>
            <TableCell>{{ formatPhoneNumber(user.phone) }}</TableCell>
            <TableCell>{{ dateFormat(user.createAt, "DD MMM YYYY") }}</TableCell>

            <TableCell>
              <Badge :variant="getBadgeVariant(user.status)">{{ user.status }}</Badge>
            </TableCell>

            <TableCell>
              <Menubar class="justify-center p-0 bg-transparent">
                <MenubarMenu>
                  <MenubarTrigger class="p-1 w-6 h-6 rounded-sm bg-slate-100 dark:bg-slate-800">
                    <Icon name="Ellipsis" :size="18" />
                  </MenubarTrigger>

                  <MenubarContent align="end">
                    <MenubarItem
                      :as="RouterLink"
                      :to="`/users/${user.id}`"
                      class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!">
                      <Icon name="Eye" :size="18" class="text-muted" /> View
                    </MenubarItem>

                    <MenubarItem
                      class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover!"
                      @click="deleteUser(user.id)">
                      <Icon name="Trash" :size="18" class="text-muted" /> Delete
                    </MenubarItem>
                  </MenubarContent>
                </MenubarMenu>
              </Menubar>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Scrollbar>

    <!-- User Table Pagination -->
    <TablePagination
      v-if="users.length > 0"
      :total="meta.total"
      :lastIndex="meta.lastIndex"
      :firstIndex="meta.firstIndex"
      v-model="filters.currentPage" />
  </Card>
</template>
