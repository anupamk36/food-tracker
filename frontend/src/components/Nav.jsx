import { Link, useNavigate } from 'react-router-dom'
import { clearToken, getToken } from '../services/auth'

export default function Nav() {
  const nav = useNavigate()
  const logout = () => {
    clearToken()
    nav('/login')
  }
  const authed = !!getToken()
  return (
    <nav className="bg-white shadow-sm sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-semibold text-xl">🥗 Food Tracker</Link>
        <div className="space-x-3">
          {authed && <Link to="/upload" className="btn">Upload</Link>}
          {authed && <button onClick={logout} className="btn bg-gray-200 text-gray-800 hover:bg-gray-300">Logout</button>}
        </div>
      </div>
    </nav>
  )
}
