import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

const el = document.getElementById("root");
if (!el) {
  const fallback = document.createElement("div");
  fallback.textContent = "Root element missing.";
  document.body.appendChild(fallback);
} else {
  createRoot(el).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
