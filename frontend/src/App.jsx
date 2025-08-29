import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ErrorBoundary from "./components/ErrorBoundary";
import Nav from "./components/Nav";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Login from "./pages/Login";
import Register from "./pages/Register";
import RequireAuth from "./components/RequireAuth";

export default function App() {
    return (
        <BrowserRouter>
            <ErrorBoundary>
                <div className="min-h-screen bg-gray-50">
                    <Nav />
                    <div className="max-w-6xl mx-auto px-4 py-6">
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />
                            <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
                            <Route path="/upload" element={<RequireAuth><Upload /></RequireAuth>} />
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </Routes>
                    </div>
                </div>
            </ErrorBoundary>
        </BrowserRouter>
    );
}
