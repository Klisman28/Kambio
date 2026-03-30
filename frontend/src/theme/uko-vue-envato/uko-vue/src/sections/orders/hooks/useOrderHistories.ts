import { onMounted, ref } from "vue";
import axios from "axios";

// ==============================================================
interface OrderHistory {
  id: number;
  title: string;
  icon: string;
  color: string;
  totalOrder: number;
}
// ==============================================================

export const useOrderHistories = () => {
  const orderHistories = ref<OrderHistory[]>([]);
  const isLoading = ref(false);
  const error = ref("");

  const getOrderHistories = async () => {
    try {
      isLoading.value = true;
      const { data } = await axios.get<OrderHistory[]>("/api/orders/histories");
      if (data) orderHistories.value = data;
    } catch (err) {
      error.value = "Something went wrong!";
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(getOrderHistories);

  return { orderHistories, isLoading, error };
};
