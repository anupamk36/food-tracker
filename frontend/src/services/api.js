import axios from 'axios'

const base = import.meta.env.VITE_API_BASE || '/api'

export const api = axios.create({
  baseURL: base,
})

export function setAuth(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}
