import { onMounted, ref } from "vue";
import axios from "axios";

export const useOrderAnalytics = () => {
  const orderAnalytics = ref<number[]>([]);
  const isLoading = ref(false);
  const error = ref("");

  const getOrderAnalytics = async () => {
    try {
      isLoading.value = true;
      const { data } = await axios.get<number[]>("/api/orders/analytics");
      if (data) orderAnalytics.value = data;
    } catch (err) {
      error.value = "Something went wrong!";
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(getOrderAnalytics);

  return { orderAnalytics, isLoading, error };
};
