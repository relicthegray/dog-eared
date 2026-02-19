import { RouteObject } from "react-router-dom";
import Login from "../pages/Login";
import Inbox from "../pages/Inbox";
import Capture from "../pages/Capture";
import Reading from "../pages/Reading";
import Owned from "../pages/Owned";
import Queue from "../pages/Queue";
import Resolve from "../pages/Resolve";
import Settings from "../pages/Settings";
import RequireAuth from "../components/RequireAuth";

const authed = (el: JSX.Element) => <RequireAuth>{el}</RequireAuth>;

export const routes: RouteObject[] = [
  { path: "/login", element: <Login /> },
  { path: "/", element: authed(<Inbox />) },
  { path: "/capture", element: authed(<Capture />) },
  { path: "/resolve", element: authed(<Resolve />) },
  { path: "/reading", element: authed(<Reading />) },
  { path: "/owned", element: authed(<Owned />) },
  { path: "/queue", element: authed(<Queue />) },
  { path: "/settings", element: authed(<Settings />) },
];
