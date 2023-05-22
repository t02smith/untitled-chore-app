import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useDetails = defineStore("userDetails", () => {
    const name = ref("");
    const uname = ref("");
    const pwd = ref("");
    function setDetails(username, password) {
        uname.value = username;
        pwd.value = password;
        console.log('[PINIA] User: ' + username)
    }

    return { name, uname, pwd, setDetails };
});
