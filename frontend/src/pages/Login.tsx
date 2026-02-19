import { useState } from "react";
import { apiPost } from "../app/api";
import { setToken } from "../app/auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const res = await apiPost<{ access_token: string }>("/auth/login", { email, password });
      setToken(res.access_token);
      nav("/", { replace: true });
    } catch (err: any) {
      setError(err?.message ?? "Login failed");
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-md px-4 py-10">
        <h1 className="text-3xl font-bold">Dog-Eared</h1>
        <p className="mt-2 text-slate-600">A cozy home for your TBR.</p>

        <form onSubmit={onSubmit} className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
          <label className="block text-sm font-medium">Email</label>
          <input
            className="mt-1 w-full rounded-xl border px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />

          <label className="mt-4 block text-sm font-medium">Password</label>
          <input
            type="password"
            className="mt-1 w-full rounded-xl border px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

          <button className="mt-6 w-full rounded-xl bg-slate-900 px-4 py-2 text-white">
            Sign in
          </button>

          <p className="mt-4 text-xs text-slate-500">
            Invite-only for now. (Open registration can be enabled later.)
          </p>
        </form>
      </div>
    </div>
  );
}
