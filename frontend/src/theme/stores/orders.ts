import { onMounted, reactive, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import { defineStore } from "pinia";
import { push } from "notivue";
import axios from "axios";
// TYPES
import { Meta } from "@/theme/types/Meta";
import { Order } from "@/theme/types/Order";

// ==============================================================
interface Data {
  meta: Meta;
  orders: Order[];
}

interface State extends Data {
  error: string;
  isLoading: boolean;
  filters: {
    search: string;
    status: string;
    payment: string;
    currentPage: number;
  };
}
// ==============================================================

export const useOrders = defineStore("orders", () => {
  const state = reactive<State>({
    orders: [],
    error: "",
    isLoading: false,
    filters: { search: "", status: "all", payment: "all", currentPage: 1 },
    meta: { page: 0, total: 0, totalPages: 0, firstIndex: 0, lastIndex: 0 }
  });

  const getOrders = async () => {
    try {
      state.isLoading = true;
      const { data } = await axios.get<Data>("/api/orders", {
        params: {
          search: state.filters.search,
          page: state.filters.currentPage,
          status: state.filters.status === "all" ? "" : state.filters.status,
          payment: state.filters.payment === "all" ? "" : state.filters.payment
        }
      });

      state.orders = data.orders;
      state.meta = data.meta;
    } catch (error) {
      console.log(error);
      state.error = "Something went wrong";
    } finally {
      state.isLoading = false;
    }
  };

  onMounted(getOrders);

  // WATCH THE CURRENT PAGE
  watch(() => state.filters.currentPage, getOrders);

  // WATCH THE ORDER STATUS
  watch(() => state.filters.status, getOrders);

  // WATCH THE ORDER SEARCH VALUE
  watchDebounced(() => state.filters.search, getOrders, { debounce: 500, maxWait: 1000 });

  const resetFilter = () => {
    state.filters.search = "";
    state.filters.status = "all";
    state.filters.currentPage = 1;
  };

  const deleteOrder = async (id: number) => {
    try {
      await axios.delete("/api/orders", { params: { id } });
      state.orders = state.orders.filter((order) => order.id !== id);
      push.success("Order deleted successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  return { state, resetFilter, deleteOrder, getOrders };
});
