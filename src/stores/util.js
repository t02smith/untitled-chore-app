import { useUserStore } from "./user";

export function handleResponse(response, expectedStatus) {
  const user = useUserStore();

  if (response.status === 401) {
    user.accessToken = null;
  }

  if (response.status !== expectedStatus) return null;
  return response.data;
}
