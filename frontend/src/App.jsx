import React, { useEffect } from "react";
import { Link, Outlet, useNavigate } from "react-router-dom";
import { setAuthToken } from "./api";

export default function App() {
  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem("token");
    setAuthToken(token);
  }, []);
  const logout = () => {
    localStorage.removeItem("token"); setAuthToken(null); navigate("/login");
  };
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold">Food Nutrition Tracker</h1>
        <nav>
          <Link className="mr-4" to="/">Upload</Link>
          <Link className="mr-4" to="/history">History</Link>
          <button onClick={logout} className="text-sm text-red-500">Logout</button>
        </nav>
      </header>
      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
