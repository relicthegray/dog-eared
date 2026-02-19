import { getToken } from "./auth";

const inferredHost = window.location.hostname;
const inferredApiBase =
  inferredHost === "localhost" ? "http://localhost:8000" : `http://${inferredHost}:8000`;

const API_BASE = import.meta.env.VITE_API_BASE ?? inferredApiBase;


function authHeaders(): HeadersInit {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { ...authHeaders() },
  });
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || `POST ${path} failed`);
  }
  return res.json();
}

export { API_BASE };
