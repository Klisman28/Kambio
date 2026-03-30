import { onMounted, reactive, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import { defineStore } from "pinia";
import { push } from "notivue";
import axios from "axios";
// TYPES
import { Invoice, InvoicePayload } from "@/types/Invoice";
import { Meta } from "@/types/Meta";

// ==============================================================
interface Data {
  meta: Meta;
  invoices: Invoice[];
}

interface State extends Data {
  error: string;
  isLoading: boolean;
  filters: { search: string; status: string; currentPage: number };
}
// ==============================================================

export const useInvoices = defineStore("invoices", () => {
  const state = reactive<State>({
    invoices: [],
    error: "",
    isLoading: false,
    filters: { search: "", status: "all", currentPage: 1 },
    meta: { page: 0, total: 0, totalPages: 0, firstIndex: 0, lastIndex: 0 }
  });

  const getInvoices = async () => {
    try {
      state.isLoading = true;
      const { data } = await axios.get<Data>("/api/invoices", {
        params: {
          search: state.filters.search,
          page: state.filters.currentPage,
          status: state.filters.status === "all" ? "" : state.filters.status
        }
      });

      state.invoices = data.invoices;
      state.meta = data.meta;
    } catch (error) {
      console.log(error);
      state.error = "Something went wrong";
    } finally {
      state.isLoading = false;
    }
  };

  onMounted(getInvoices);

  // WATCH THE CURRENT PAGE
  watch(() => state.filters.currentPage, getInvoices);

  // WATCH THE INVOICE STATUS
  watch(() => state.filters.status, getInvoices);

  // WATCH THE INVOICE SEARCH VALUE
  watchDebounced(() => state.filters.search, getInvoices, { debounce: 500, maxWait: 1000 });

  const resetFilter = () => {
    state.filters.search = "";
    state.filters.status = "all";
    state.filters.currentPage = 1;
  };

  const deleteInvoice = async (id: string) => {
    try {
      await axios.delete("/api/invoices", { params: { id } });
      state.invoices = state.invoices.filter((invoice) => invoice.id !== id);
      push.success("Invoice deleted successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const createNewInvoice = async (body: InvoicePayload) => {
    try {
      const items = body.products.reduce((acc, item) => acc + (item.total || 0), 0);

      const newInvoice = {
        ...body,
        issueDate: new Date().toDateString(),
        totalAmount: items + body.tax! + body.shippingCharge!
      };

      const { data } = await axios.post<{ invoice: Invoice }>("/api/invoices", newInvoice);
      state.invoices.unshift(data.invoice);
      push.success("Invoice created successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const updateInvoice = async (id: string, body: InvoicePayload) => {
    try {
      await axios.put("/api/invoices", body, { params: { id } });
      push.success("Invoice updated successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  return {
    state,
    resetFilter,
    deleteInvoice,
    updateInvoice,
    createNewInvoice
  };
});
