import axios from "axios";

export const httpClient = axios.create({
  baseURL: "/api/github",
  timeout: 10000, // 10 seconds timeout
  withCredentials: true,
});
