import { Link, useLocation, useNavigate } from "react-router-dom";
import { isAuthed, clearToken } from "../services/auth";
import { setAuth } from "../services/api";

export default function Nav() {
  const { pathname } = useLocation();
  const nav = useNavigate();
  const authed = isAuthed();

  function logout() {
    clearToken();
    setAuth(null);
    nav("/login");
  }

  const Item = ({ to, children }) => (
    <Link className={`mr-3 btn ${pathname === to ? "opacity-90" : ""}`} to={to}>{children}</Link>
  );

  return (
    <div className="w-full bg-white shadow">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center">
          <div className="font-semibold mr-4">Food Tracker</div>
          <Item to="/">Home</Item>
          {authed && <Item to="/dashboard">Dashboard</Item>}
          {authed && <Item to="/upload">Upload</Item>}
        </div>
        <div>
          {!authed ? (
            <>
              <Item to="/login">Login</Item>
              <Item to="/register">Register</Item>
            </>
          ) : (
            <button className="btn" onClick={logout}>Logout</button>
          )}
        </div>
      </div>
    </div>
  );
}
