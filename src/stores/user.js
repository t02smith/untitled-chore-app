import { ref, onMounted, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { handleResponse } from "./util";

export const useUserStore = defineStore("users", () => {
  const user = ref(null);
  const accessToken = ref(null);

  const error = ref(null);

  onMounted(() => {
    const token = localStorage.getItem("access_token");
    if (token === null) return;

    accessToken.value = token;
  });

  watch(accessToken, () => {
    localStorage.setItem("access_token", accessToken.value);
  });

  async function getUserData() {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE}/me`, {
      headers: { Authorization: `Bearer ${accessToken.value}` },
      validateStatus: () => true,
    });

    if (!handleResponse(res, 200)) return null;

    user.value = res.data;
    return res.data;
  }

  async function login(username, password) {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE}/login`,
      `username=${username}&password=${password}`,
      { validateStatus: () => true }
    );

    if (!handleResponse(res, 201)) return null;

    accessToken.value = res.data.access_token;
    user.value = res.data.user;
    return true;
  }

  async function register(username, password, firstName, surname, email) {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE}/register`,
      {
        username: username,
        password: password,
        first_name: firstName,
        surname: surname,
        email: email,
      },
      { validateStatus: () => true }
    );

    if (res.status !== 201) return false;

    accessToken.value = res.data.access_token;
    return true;
  }

  return { user, login, accessToken, register, error, getUserData };
});