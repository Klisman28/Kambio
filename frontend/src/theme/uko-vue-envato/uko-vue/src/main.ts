import { createApp } from "vue";
import { createPinia } from "pinia";
import { createNotivue } from "notivue";
import VueApexCharts from "vue3-apexcharts";

// THIRD PARTY CSS
import "simplebar-vue/dist/simplebar.min.css";
import "notivue/notification.css";
import "notivue/animations.css";
import "nprogress/nprogress.css";

// MAIN CSS
import "@/assets/index.css";

// FAKE API
import "./__mock__";

// ROOT FILE
import App from "./App.vue";

// ROUTER
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(VueApexCharts);
app.use(createNotivue());
app.use(router);

app.mount("#app");
