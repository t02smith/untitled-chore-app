import { ref, watch, onMounted } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import qs from "qs";

export const useUserStore = defineStore("users", () => {
  const user = ref(null);
  const accessToken = ref(null);

  // check if access token is stored
  onMounted(() => (accessToken.value = localStorage.getItem("access_token")));

  async function login(username, password) {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE}/login`,
      `username=${username}&password=${password}`
    );

    accessToken.value = res.data.access_token;
    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("access_token_expiry", red.data.expiry);
  }

  async function register(username, password, firstName, surname, email) {
    const res = await axios.post(`${import.meta.env.VITE_API_BASE}/register`, {
      username: username,
      password: password,
      first_name: firstName,
      surname: surname,
      email: email,
    });

    accessToken.value = res.data.access_token;
  }

  return { user, login, accessToken, register };
});
