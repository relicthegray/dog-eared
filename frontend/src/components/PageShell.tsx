import { ReactNode } from "react";
import BottomNav from "./BottomNav";
import { Link } from "react-router-dom";

export default function PageShell({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="min-h-screen pb-20">
      <header className="sticky top-0 z-10 border-b bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-xl items-center justify-between px-4 py-3">
          <h1 className="text-lg font-semibold">{title}</h1>
          <Link to="/settings" className="text-sm text-slate-600 hover:text-slate-900">
            Settings
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-xl px-4 py-4">{children}</main>

      <BottomNav />
    </div>
  );
}
