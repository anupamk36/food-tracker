import { useState } from "react";
import { api, setAuth } from "../services/api";
import { getToken } from "../services/auth";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [notes, setNotes] = useState("");
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    setMsg("");
    setAuth(getToken?.());
    const form = new FormData();
    if (file) form.append("file", file);
    if (notes) form.append("notes", notes);
    await api.post("/meals/", form, { headers: { "Content-Type": "multipart/form-data" } });
    setMsg("Uploaded! Analysis will be ready shortly.");
    setFile(null); setNotes("");
  }

  return (
    <div className="card max-w-xl">
      <h1 className="text-xl font-semibold mb-4">Upload Meal</h1>
      <form onSubmit={submit} className="space-y-4">
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <textarea className="input" placeholder="Notes (optional)" value={notes} onChange={(e) => setNotes(e.target.value)} />
        <button className="btn" type="submit">Upload</button>
      </form>
      {msg && <div className="mt-3 text-green-700">{msg}</div>}
    </div>
  );
}
