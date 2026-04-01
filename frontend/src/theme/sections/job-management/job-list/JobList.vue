<script setup lang="ts">
import Scrollbar from "simplebar-vue";
// SHADCN COMPONENTS
import { Card, CardTitle } from "@/theme/components/ui/card";
import {
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableHeader
} from "@/theme/components/ui/table";
import {
  Menubar,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent
} from "@/theme/components/ui/menubar";
// CUSTOM COMPONENT
import Icon from "@/theme/components/Icon.vue";
// CUSTOM DATA
import { jobList } from "@/theme/data/dashboards/job-management";
</script>

<template>
  <Card class="col-span-full pt-6 pb-2 2xl:col-span-8 xl:col-span-7 lg:col-span-7 self-start">
    <CardTitle class="px-5 mb-8">Job List</CardTitle>

    <Scrollbar>
      <Table class="min-w-[600px]">
        <TableHeader>
          <TableRow>
            <TableHead>Posts</TableHead>
            <TableHead>Posted at</TableHead>
            <TableHead class="text-center">Applicants</TableHead>
            <TableHead class="text-center">Actions</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <TableRow v-for="job in jobList" :key="job.id">
            <TableCell class="py-2">
              {{ job.jobTitle }}
            </TableCell>

            <TableCell class="py-2">{{ job.postedAt }}</TableCell>
            <TableCell class="py-2 text-center">{{ job.applicants }} </TableCell>

            <TableCell class="py-2">
              <Menubar class="justify-center p-0 bg-transparent">
                <MenubarMenu>
                  <MenubarTrigger class="p-1 w-6 h-6 rounded-sm bg-slate-100 dark:bg-slate-800">
                    <Icon name="Ellipsis" :size="18" />
                  </MenubarTrigger>

                  <MenubarContent align="end">
                    <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover">
                      <Icon name="Eye" :size="18" class="text-muted" /> View
                    </MenubarItem>

                    <MenubarItem class="gap-2 px-4 py-2 text-[13px] font-medium hover:bg-hover">
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
  </Card>
</template>
