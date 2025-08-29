import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { api, setAuth } from "../services/api";
import { saveToken } from "../services/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();
  const loc = useLocation();
  const from = loc.state?.from?.pathname || "/dashboard";

  async function submit(e) {
    e.preventDefault();
    setErr(""); setLoading(true);
    try {
      const { data } = await api.post("/auth/login", { email, password });
      const token = data?.access_token || data?.token;
      if (!token) throw new Error("No access token returned");
      saveToken(token);
      setAuth(token);
      nav(from, { replace: true });
    } catch (e2) {
      setErr(e2?.response?.data?.detail || e2.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center">
      <div className="max-w-md mx-auto w-full card">
        <h1 className="text-2xl font-semibold mb-4">Login</h1>
        {err && <div className="mb-3 text-red-600">{err}</div>}
        <form onSubmit={submit} className="space-y-3">
          <input className="input" type="email" placeholder="Email"
            value={email} onChange={e => setEmail(e.target.value)} required />
          <input className="input" type="password" placeholder="Password"
            value={password} onChange={e => setPassword(e.target.value)} required />
          <button className="btn w-full" disabled={loading}>{loading ? "Signing in..." : "Sign in"}</button>
        </form>
        <div className="mt-3 text-sm">
          New here? <Link className="text-indigo-600 underline" to="/register">Create an account</Link>
        </div>
      </div>
    </div>
  );
}
