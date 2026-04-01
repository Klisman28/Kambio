<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
// SHADCN COMPONENTS
import {
  Dialog,
  DialogTitle,
  DialogClose,
  DialogFooter,
  DialogHeader,
  DialogContent,
  DialogTrigger,
  DialogDescription
} from "@/theme/components/ui/dialog";
import { Button } from "@/theme/components/ui/button";
import { Textarea } from "@/theme/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/theme/components/ui/avatar";
// CUSTOM COMPONENTS
import Icon from "@/theme/components/Icon.vue";
import Rating from "@/theme/components/Rating.vue";
// TYPES
import { Product, Review } from "@/theme/types/Product";

const { product } = defineProps<{ product: Product }>();

const error = ref("");
const isLoading = ref(false);
const reviews = ref<Review[]>([]);

const getReviews = async () => {
  try {
    isLoading.value = true;
    const { data } = await axios.get<Review[]>("/api/reviews", { params: { id: product.id } });
    if (data) reviews.value = data;
  } catch (err) {
    console.log(err);
    error.value = "Something went wrong!";
  } finally {
    isLoading.value = false;
  }
};

onMounted(getReviews);
</script>

<template>
  <div class="pt-8">
    <div class="flex flex-wrap items-center justify-between gap-4 pb-5 mb-5 border-b border-border">
      <p class="text-sm font-semibold underline">Ratings & Reviews</p>

      <div class="flex items-center gap-2">
        <Rating :rating="product.rating" />
        <p>({{ product.rating }} out of 5)</p>
        <p class="text-muted">{{ product.totalReviews }} total ratings</p>
      </div>
    </div>

    <!-- REVIEW CREATE BUTTON & DIALOG -->
    <div class="flex items-center justify-between mb-4">
      <p class="mb-2 text-sm font-semibold">Reviews</p>

      <Dialog>
        <DialogTrigger as-child>
          <Button>Add Review</Button>
        </DialogTrigger>

        <DialogContent>
          <DialogHeader>
            <DialogTitle>Write your public review</DialogTitle>
            <DialogDescription>
              Make changes to your profile here. Click save when you're done.
            </DialogDescription>
          </DialogHeader>

          <div class="items-center space-y-4">
            <div class="flex items-center gap-1 text-sm">
              <Rating :rating="0" />
              <p>(0)</p>
            </div>

            <Textarea
              rows="8"
              id="review"
              value=""
              placeholder="Write your review here..."></Textarea>
          </div>

          <DialogFooter class="gap-2">
            <DialogClose as-child>
              <Button color="error">Cancel</Button>
            </DialogClose>

            <Button>Publish</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <!-- REVIEW LIST -->
    <div
      class="pb-5 mb-5 space-y-2 border-b border-border last:border-b-0 last:mb-0"
      v-for="review in reviews">
      <div class="flex items-center gap-3 mb-3">
        <Avatar shape="square">
          <AvatarImage :src="review.user.image" :alt="review.user.name" />
          <AvatarFallback>{{ review.user.name[0] }}</AvatarFallback>
        </Avatar>

        <div>
          <h5 class="text-sm font-semibold leading-6">{{ review.user.name }}</h5>
          <p class="text-xs font-medium text-muted">on {{ review.createdAt }}</p>
        </div>
      </div>

      <Rating :rating="review.rating" />

      <p class="text-muted font-xs">"{{ review.review }}"</p>

      <div class="flex items-start gap-5 pt-2">
        <div class="flex items-center gap-1 text-muted">
          <Icon name="ThumbsUp" :size="17" class="leading-none text-success" />
          <p class="leading-none">{{ review.likes }}</p>
        </div>

        <div class="flex items-center gap-1 text-muted">
          <Icon name="ThumbsDown" :size="17" class="leading-none text-error" />
          <p class="leading-0">{{ review.dislikes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
