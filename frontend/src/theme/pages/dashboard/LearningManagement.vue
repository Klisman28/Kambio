<script setup lang="ts">
import Footer from "@/components/Footer.vue";
import Result from "@/sections/learning-management/result";
import IntroCard from "@/sections/learning-management/intro";
import StatusList from "@/sections/learning-management/status";
import Downloads from "@/sections/learning-management/downloads";
import UpgradeProCard from "@/sections/learning-management/upgrade-pro";
import UpcomingTask from "@/sections/learning-management/upcoming-task";
import CourseStatus from "@/sections/learning-management/course-status";
import StudyTimeLastWeek from "@/sections/learning-management/study-time";
</script>

<template>
  <div class="grid grid-cols-12 mt-2 mb-6 gap-7">
    <!-- Intro Overview Card -->
    <IntroCard />

    <!-- Upgrade to Pro Card -->
    <UpgradeProCard />

    <!-- Results Card -->
    <Result />

    <!-- Study Time Last Week Card -->
    <StudyTimeLastWeek />

    <!-- Upcoming Task -->
    <UpcomingTask />

    <!-- Different Course Status Cards -->
    <StatusList />

    <!-- Course Status -->
    <CourseStatus />

    <!-- Your Downloads -->
    <Downloads />

    <!-- Footer -->
    <Footer></Footer>
  </div>
</template>
