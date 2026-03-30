import { onMounted, ref } from "vue";
import axios from "axios";
// TYPES
import { Status } from "@/types/Status";

export const useOrderStatuses = () => {
  const statuses = ref<Status[]>([]);
  const isLoading = ref(false);
  const error = ref("");

  const getOrderStatues = async () => {
    try {
      isLoading.value = true;
      const { data } = await axios.get<Status[]>("/api/orders/statues");
      if (data) statuses.value = data;
    } catch (err) {
      error.value = "Something went wrong!";
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(getOrderStatues);

  return { statuses, isLoading, error };
};
