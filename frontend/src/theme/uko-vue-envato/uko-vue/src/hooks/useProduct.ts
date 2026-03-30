import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
// TYPES
import { Product } from "@/types/Product";

export function useProduct(productId: number) {
  const router = useRouter();

  const error = ref();
  const isLoading = ref(false);
  const product = ref<Product>();

  const getProduct = async () => {
    try {
      isLoading.value = true;
      const { data } = await axios.get<Product>("/api/products", {
        params: { id: productId }
      });

      if (data) product.value = data;
      else router.push({ name: "NotFound" });
    } catch (err) {
      error.value = "Something went wrong";
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(getProduct);

  return { error, isLoading, product };
}
