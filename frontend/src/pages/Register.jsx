import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../services/api'

export default function Register() {
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [ok, setOk] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/auth/register', { email, password })
      setOk(true)
      setTimeout(()=>nav('/login'), 800)
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="card w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6">Create your account</h1>
        <form onSubmit={submit} className="space-y-4">
          <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
          <input className="input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
          {error && <div className="text-red-600 text-sm">{error}</div>}
          {ok && <div className="text-green-700 text-sm">Registered! Redirecting…</div>}
          <button className="btn w-full">Sign up</button>
        </form>
        <div className="text-sm mt-4">Have an account? <Link to="/login" className="text-indigo-600">Sign in</Link></div>
      </div>
    </div>
  )
}
