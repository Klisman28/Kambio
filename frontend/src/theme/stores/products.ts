import { onMounted, reactive, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import { defineStore } from "pinia";
import { push } from "notivue";
import axios from "axios";
// TYPES
import { Product, ProductPayload } from "@/theme/types/Product";
import { Meta } from "@/theme/types/Meta";

// ==============================================================
interface Data {
  meta: Meta;
  products: Product[];
}

interface State extends Data {
  error: string;
  isLoading: boolean;
  filters: { search: string; status: string; currentPage: number };
}
// ==============================================================

export const useProducts = defineStore("products", () => {
  const state = reactive<State>({
    products: [],
    error: "",
    isLoading: false,
    filters: { search: "", status: "all", currentPage: 1 },
    meta: { page: 0, total: 0, totalPages: 0, firstIndex: 0, lastIndex: 0 }
  });

  const getProducts = async () => {
    try {
      state.isLoading = true;
      const { data } = await axios.get<Data>("/api/products", {
        params: {
          search: state.filters.search,
          page: state.filters.currentPage,
          status: state.filters.status === "all" ? "" : state.filters.status
        }
      });

      state.products = data.products;
      state.meta = data.meta;
    } catch (error) {
      console.log(error);
      state.error = "Something went wrong";
    } finally {
      state.isLoading = false;
    }
  };

  onMounted(async () => {
    await getProducts();
  });

  // WATCH THE CURRENT PAGE
  watch(() => state.filters.currentPage, getProducts);

  // WATCH THE PRODUCT STATUS
  watch(() => state.filters.status, getProducts);

  // WATCH THE PRODUCT SEARCH VALUE
  watchDebounced(() => state.filters.search, getProducts, { debounce: 500, maxWait: 1000 });

  const resetFilter = () => {
    state.filters.search = "";
    state.filters.status = "all";
    state.filters.currentPage = 1;
  };

  const deleteProduct = async (id: number) => {
    try {
      await axios.delete("/api/products", { params: { id } });
      state.products = state.products.filter((product) => product.id !== id);
      push.success("Product deleted successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const createNewProduct = async (body: ProductPayload) => {
    try {
      const updateBody = {
        ...body,
        rating: 0,
        discount: 0,
        totalReviews: 0,
        featureImage: body.images[0],
        createdAt: new Date().toDateString(),
        status: body.status ? "Published" : "Draft",
        id: state.products[state.products.length - 1].id + 1,
        offers: [
          "Bank Offer 10% Instant Discount on Paypal, up to $1250 on orders of $5,000 and above T&C"
        ]
      };

      const { data } = await axios.post<{ product: Product }>("/api/products", updateBody);
      state.products.push(data.product);
      push.success("Product created successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const updateProduct = async (id: number, body: ProductPayload) => {
    try {
      await axios.put<{ product: Product }>("/api/products", body, {
        params: { id }
      });

      push.success("Product updated successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  return {
    state,
    resetFilter,
    deleteProduct,
    updateProduct,
    createNewProduct
  };
});
