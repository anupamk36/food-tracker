import React, { useState } from "react";
import { api, setAuthToken } from "../api";
import { useNavigate } from "react-router-dom";

export default function Login(){
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();
  const submit = async (e) => {
    e.preventDefault();
    const resp = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", resp.data.access_token);
    setAuthToken(resp.data.access_token);
    nav("/");
  };
  return (
    <form onSubmit={submit} className="max-w-md mx-auto">
      <h2 className="text-xl mb-4">Login</h2>
      <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="input" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)}/>
      <button className="btn mt-2">Login</button>
    </form>
  );
}
