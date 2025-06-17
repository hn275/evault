import axios from "axios";

export const httpClient = axios.create({
  baseURL: "/",
  timeout: 10000, // 10 seconds timeout
});
