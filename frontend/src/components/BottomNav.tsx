import { NavLink } from "react-router-dom";

const linkBase =
  "flex flex-col items-center justify-center gap-1 px-3 py-2 text-xs rounded-xl";
const active = "bg-slate-900 text-white";
const inactive = "text-slate-700 hover:bg-slate-100";

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 border-t bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-xl items-center justify-around px-2 py-2">
        <NavLink
          to="/"
          className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
        >
          <span>Inbox</span>
        </NavLink>
        <NavLink
          to="/capture"
          className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
        >
          <span>Capture</span>
        </NavLink>
        <NavLink
          to="/reading"
          className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
        >
          <span>Reading</span>
        </NavLink>
        <NavLink
          to="/owned"
          className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
        >
          <span>Owned</span>
        </NavLink>
        <NavLink
          to="/queue"
          className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}
        >
          <span>Queue</span>
        </NavLink>
      </div>
    </nav>
  );
}
