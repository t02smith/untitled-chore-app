import { createApp } from "vue";
import { createPinia } from "pinia";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faShower,
  faCouch,
  faKitchenSet,
  faHouse,
  faStopwatch,
  faSquareCheck,
  faRefresh,
  faPlusCircle,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";
library.add(faShower, faCouch, faKitchenSet, faHouse, faRefresh, faStopwatch, faSquareCheck, faPlusCircle, faUserPlus);

const app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon);

app.use(createPinia());
app.use(router);

app.mount("#app");
