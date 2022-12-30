import axios from "axios";
import { defineStore } from "pinia";
import { useUserStore } from "./user";

export const useHomeStore = defineStore("homes", () => {
  const user = useUserStore();

  function handleResponse(response, expectedStatus) {
    if (response.status === 401) {
      user.accessToken = null;
    }

    if (response.status !== expectedStatus) return null;
    return response.data;
  }

  async function getHome(creator, homeName) {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function getHomes() {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/homes/`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function createHome(homeName, chores) {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE}/homes`,
      { name: homeName, chores: chores },
      { headers: { Authorization: `Bearer ${user.accessToken}` } }
    );

    return handleResponse(res, 201);
  }

  async function joinHome(creator, homeName, inviteId) {
    const res = await axios.put(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/join?invite_id=${inviteId}`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function createInviteLink(creator, homeName) {
    const res = await axios.post(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/invite`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 201);
  }

  async function getHomesChores(creator, homeName) {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/chores`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function getHomeResidents(creator, homeName) {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/residents`, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function getTimetable(creator, homeName) {
    const res = await axios.put(`${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/timetable`, null, {
      headers: { Authorization: `Bearer ${user.accessToken}` },
      validateStatus: () => true,
    });

    return handleResponse(res, 200);
  }

  async function completeChore(creator, homeName, choreId) {
    const res = await axios.put(
      `${import.meta.env.VITE_API_BASE}/${creator}/${homeName}/complete?chore_id=${choreId}`,
      null,
      {
        headers: { Authorization: `Bearer ${user.accessToken}` },
        validateStatus: () => true,
      }
    );

    return handleResponse(res, 200);
  }

  return {
    getHome,
    getHomes,
    getHomesChores,
    getHomeResidents,
    createHome,
    createInviteLink,
    joinHome,
    getTimetable,
    completeChore,
  };
});
