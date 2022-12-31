import axios from "axios";
import { defineStore } from "pinia";
import { useUserStore } from "./user";
import { handleResponse } from "./util";

export const useChoreStore = defineStore("chores", () => {
  const user = useUserStore();

  async function getDefaultChores() {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/chores/default`, { validateStatus: () => true });

    return handleResponse(res, 200);
  }

  return { getDefaultChores };
});
