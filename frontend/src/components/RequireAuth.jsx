import { Navigate, useLocation } from "react-router-dom";
import { isAuthed } from "../services/auth";

export default function RequireAuth({ children }) {
    const loc = useLocation();
    if (!isAuthed()) {
        return <Navigate to="/login" replace state={{ from: loc }} />;
    }
    return children;
}
