<script setup lang="ts">
import Footer from "@/theme/components/Footer.vue";
import Result from "@/theme/sections/learning-management/result";
import IntroCard from "@/theme/sections/learning-management/intro";
import StatusList from "@/theme/sections/learning-management/status";
import Downloads from "@/theme/sections/learning-management/downloads";
import UpgradeProCard from "@/theme/sections/learning-management/upgrade-pro";
import UpcomingTask from "@/theme/sections/learning-management/upcoming-task";
import CourseStatus from "@/theme/sections/learning-management/course-status";
import StudyTimeLastWeek from "@/theme/sections/learning-management/study-time";
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
