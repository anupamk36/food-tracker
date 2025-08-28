import React, { useEffect, useState } from "react";
import { api } from "../api";

export default function History() {
  const [meals, setMeals] = useState([]);
  useEffect(() => { fetchMeals(); }, []);
  async function fetchMeals() {
    const resp = await api.get("/meals/");
    setMeals(resp.data);
  }
  return (
    <div>
      <h2 className="text-lg mb-4">Meal History</h2>
      <table className="table-auto w-full">
        <thead><tr><th>Date</th><th>Status</th><th>Calories</th><th>Details</th></tr></thead>
        <tbody>
          {meals.map(m => (
            <tr key={m.id}>
              <td>{new Date(m.timestamp).toLocaleString()}</td>
              <td>{m.status}</td>
              <td>{m.nutrition?.calories ? Math.round(m.nutrition.calories) : "-"}</td>
              <td><a href={`${m.image_path}`} target="_blank">Image</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
