<script setup lang="ts">
import Footer from "@/components/Footer.vue";
import Result from "@/sections/job-management/result";
import JobList from "@/sections/job-management/job-list";
import Analytics from "@/sections/job-management/analytics";
import UpgradeToPro from "@/sections/job-management/upgrade-pro";
import CandidatesByGender from "@/sections/job-management/candidates";
import RecentJobApplication from "@/sections/job-management/recent-job";
import ProfileOverview from "@/sections/job-management/profile-overview";
import ApplicationReceivedTime from "@/sections/job-management/received-time";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <div class="grid grid-cols-12 col-span-full 2xl:col-span-8 xl:col-span-8 gap-7">
      <Analytics />

      <!-- Recent Job Applications -->
      <RecentJobApplication />

      <!-- Result -->
      <Result />
    </div>

    <!-- User Profile Overview Card -->
    <ProfileOverview />

    <!-- Job List Table  -->
    <JobList />

    <!-- Candidates By Gender Graph -->
    <CandidatesByGender />

    <!-- Application Received Time Graph  -->
    <ApplicationReceivedTime />

    <!-- Upgrade to Pro Card -->
    <UpgradeToPro />

    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>
