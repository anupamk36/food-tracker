import axios from "axios";
import { getToken } from "./auth";

const raw = import.meta.env?.VITE_API_BASE;
const base = (raw && raw.trim()) || "/api";

export const api = axios.create({ baseURL: base.replace(/\/+$/, "") });

export function setAuth(token) {
  if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`;
  else delete api.defaults.headers.common.Authorization;
}

// initialize on import
setAuth(getToken());
