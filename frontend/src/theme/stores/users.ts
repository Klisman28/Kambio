import { onMounted, reactive, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import { defineStore } from "pinia";
import { push } from "notivue";
import axios from "axios";
// TYPES
import { User, UserPayload } from "@/theme/types/User";
import { Meta } from "@/theme/types/Meta";

// ==============================================================
interface Data {
  meta: Meta;
  users: User[];
}

interface State extends Data {
  error: string;
  isLoading: boolean;
  filters: { search: string; status: string; currentPage: number };
}
// ==============================================================

export const useUsers = defineStore("users", () => {
  const state = reactive<State>({
    users: [],
    error: "",
    isLoading: false,
    filters: { search: "", status: "all", currentPage: 1 },
    meta: { page: 0, total: 0, totalPages: 0, firstIndex: 0, lastIndex: 0 }
  });

  const getUsers = async () => {
    try {
      state.isLoading = true;
      const { data } = await axios.get<Data>("/api/users", {
        params: {
          page: state.filters.currentPage,
          search: state.filters.search,
          status: state.filters.status === "all" ? "" : state.filters.status
        }
      });

      state.users = data.users;
      state.meta = data.meta;
    } catch (error) {
      console.log(error);
      state.error = "Something went wrong";
    } finally {
      state.isLoading = false;
    }
  };

  onMounted(async () => {
    await getUsers();
  });

  // WATCH THE CURRENT PAGE
  watch(() => state.filters.currentPage, getUsers);

  // WATCH THE USER STATUS
  watch(() => state.filters.status, getUsers);

  // WATCH THE USER SEARCH VALUE
  watchDebounced(() => state.filters.search, getUsers, { debounce: 500, maxWait: 1000 });

  const resetFilter = () => {
    state.filters.search = "";
    state.filters.status = "all";
    state.filters.currentPage = 1;
  };

  const getUserById = (id: number) => {
    return axios.get<User>("/api/users", { params: { id } });
  };

  const deleteUser = async (id: number) => {
    try {
      await axios.delete("/api/users", { params: { id } });
      state.users = state.users.filter((item) => item.id !== id);
      push.success("User deleted successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const createNewUser = async (body: UserPayload) => {
    try {
      const { data } = await axios.post<{ user: User }>("/api/users", body);
      state.users.push(data.user);
      push.success("User created successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  const updateUser = async (id: number, body: UserPayload) => {
    try {
      await axios.put<{ user: User }>("/api/users", body, {
        params: { id }
      });

      // const index = state.users.findIndex((item) => item.id === id);
      // state.users[index] = data.user;
      push.success("User updated successfully");
    } catch (error) {
      console.log(error);
      push.error("Something went wrong");
    }
  };

  return { state, resetFilter, deleteUser, getUserById, createNewUser, updateUser };
});
