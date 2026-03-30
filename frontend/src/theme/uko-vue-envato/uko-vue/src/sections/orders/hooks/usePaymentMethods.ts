import { onMounted, ref } from "vue";
import axios from "axios";
// TYPES
interface PaymentMethod {
  id: number;
  title: string;
  value: string;
}

export const usePaymentMethods = () => {
  const paymentMethods = ref<PaymentMethod[]>([]);
  const isLoading = ref(false);
  const error = ref("");

  const getPaymentMethods = async () => {
    try {
      isLoading.value = true;
      const { data } = await axios.get<PaymentMethod[]>("/api/orders/payment-methods");
      if (data) paymentMethods.value = data;
    } catch (err) {
      error.value = "Something went wrong!";
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(getPaymentMethods);

  return { paymentMethods, isLoading, error };
};
