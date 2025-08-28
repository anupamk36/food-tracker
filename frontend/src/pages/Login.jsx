import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { saveToken } from '../services/auth'
import Nav from '../components/Nav'

export default function Login() {
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const res = await api.post('/auth/login', { email, password })
      saveToken(res.data.access_token)
      nav('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen">
      <Nav/>
      <div className="max-w-md mx-auto mt-12 card">
        <h1 className="text-2xl font-semibold mb-6">Welcome back</h1>
        <form onSubmit={submit} className="space-y-4">
          <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
          <input className="input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
          {error && <div className="text-red-600 text-sm">{error}</div>}
          <button className="btn w-full">Sign in</button>
        </form>
        <div className="text-sm mt-4">No account? <Link to="/register" className="text-indigo-600">Create one</Link></div>
      </div>
    </div>
  )
}
