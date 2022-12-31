import { useUserStore } from "./user";

export function handleResponse(response, expectedStatus) {
  const user = useUserStore();

  if (response.status === 401) {
    user.accessToken = null;
    return null;
  }

  if (response.status !== expectedStatus) {
    user.error = response.data.detail;
    return null;
  }

  user.error = null;
  return response.data;
}
