import axios from "axios";
import { defineStore } from "pinia";
import { useUserStore } from "./user";

export const useTimetableStore = defineStore("timetable", () => {
  const user = useUserStore();

  async function getTimetable(creator, homeName) {
    return (
      await axios.put(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/timetable`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  async function completeChore(creator, homeName, choreId) {
    return (
      await axios.put(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/complete?chore_id=${choreId}`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  return { getTimetable, completeChore };
});
