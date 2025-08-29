import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../services/api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [err, setErr] = useState("");
  const [ok, setOk] = useState("");
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setErr(""); setOk(""); setLoading(true);
    try {
      if (password !== confirm) throw new Error("Passwords do not match");
      await api.post("/auth/register", { email, password });
      setOk("Account created — please log in.");
      setTimeout(() => nav("/login"), 600);
    } catch (e2) {
      setErr(e2?.response?.data?.detail || e2.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center">
      <div className="max-w-md mx-auto w-full card">
        <h1 className="text-2xl font-semibold mb-4">Create account</h1>
        {err && <div className="mb-3 text-red-600">{err}</div>}
        {ok && <div className="mb-3 text-green-600">{ok}</div>}
        <form onSubmit={submit} className="space-y-3">
          <input className="input" type="email" placeholder="Email"
            value={email} onChange={e => setEmail(e.target.value)} required />
          <input className="input" type="password" placeholder="Password"
            value={password} onChange={e => setPassword(e.target.value)} required />
          <input className="input" type="password" placeholder="Confirm password"
            value={confirm} onChange={e => setConfirm(e.target.value)} required />
          <button className="btn w-full" disabled={loading}>{loading ? "Creating..." : "Create account"}</button>
        </form>
        <div className="mt-3 text-sm">
          Already have an account? <Link className="text-indigo-600 underline" to="/login">Log in</Link>
        </div>
      </div>
    </div>
  );
}
