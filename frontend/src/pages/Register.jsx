import React, { useState } from "react";
import { api } from "../api";
import { useNavigate } from "react-router-dom";

export default function Register(){
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();
  const submit = async (e) => {
    e.preventDefault();
    await api.post("/auth/register", { email, password });
    nav("/login");
  };
  return (
    <form onSubmit={submit} className="max-w-md mx-auto">
      <h2 className="text-xl mb-4">Register</h2>
      <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="input" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)}/>
      <button className="btn mt-2">Register</button>
    </form>
  );
}
