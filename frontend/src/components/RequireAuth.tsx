import { Navigate, useLocation } from "react-router-dom";
import { getToken } from "../app/auth";

export default function RequireAuth({ children }: { children: JSX.Element }) {
  const token = getToken();
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return children;
}
