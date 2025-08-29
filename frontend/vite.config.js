import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const proxy = {
  "/api": { target: "http://backend:8000", changeOrigin: true },
  "/uploads": { target: "http://backend:8000", changeOrigin: true },
};

export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 5173, proxy },
  preview: { host: true, port: 5173, proxy },
});
