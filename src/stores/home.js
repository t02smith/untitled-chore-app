import axios from "axios";
import { defineStore } from "pinia";
import { useUserStore } from "./user";

export const useHomeStore = defineStore("homes", () => {
  const user = useUserStore();

  async function getHome(creator, homeName) {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
    });

    return res.data;
  }

  async function getHomes() {
    return (
      await axios.get(`${import.meta.env.VITE_API_BASE}/homes/`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  async function createHome(homeName, chores) {
    return (
      await axios.post(
        `${import.meta.env.VITE_API_BASE}/homes`,
        { name: homeName, chores: chores },
        { headers: { Authorization: `Bearer ${user.accessToken}` } }
      )
    ).data;
  }

  async function joinHome(creator, homeName, inviteId) {
    return (
      await axios.put(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/join?invite_id=${inviteId}`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  async function createInviteLink(creator, homeName) {
    return (
      await axios.post(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/invite`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  async function getHomesChores(creator, homeName) {
    return (
      await axios.get(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/chores`, {
        headers: { Authorization: `Bearer ${user.accessToken}` },
      })
    ).data;
  }

  return {
    getHome,
    getHomes,
    createHome,
    createInviteLink,
    joinHome,
  };
});
