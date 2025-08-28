import { useState } from 'react'
import { api, setAuth } from '../services/api'
import { getToken } from '../services/auth'
import Nav from '../components/Nav'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [notes, setNotes] = useState('')
  const [msg, setMsg] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setMsg('')
    const t = getToken()
    setAuth(t)
    const form = new FormData()
    form.append('file', file)
    if (notes) form.append('notes', notes)
    await api.post('/meals/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    setMsg('Uploaded! Check Dashboard.')
  }

  return (
    <div className="min-h-screen">
      <Nav/>
      <div className="max-w-xl mx-auto p-4">
        <div className="card">
          <h1 className="text-xl font-semibold mb-4">Upload your meal</h1>
          <form onSubmit={submit} className="space-y-3">
            <input type="file" accept="image/*" className="w-full" onChange={e=>setFile(e.target.files?.[0])} required />
            <textarea className="input h-24" placeholder="Notes (optional)" value={notes} onChange={e=>setNotes(e.target.value)} />
            <button className="btn">Upload</button>
          </form>
          {msg && <div className="text-green-700 mt-3">{msg}</div>}
        </div>
      </div>
    </div>
  )
}
