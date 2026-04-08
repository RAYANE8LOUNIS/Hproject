import { NavLink } from "react-router-dom";

function SidebarItem({ label, to }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => `sidebar-item ${isActive ? "active" : ""}`}
    >
      <span className="sidebar-icon" />
      <span>{label}</span>
    </NavLink>
  );
}

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo-wrap">
        <div className="logo-icon"></div>
        <div className="logo-text">Sky Portal</div>
      </div>

      <nav className="sidebar-nav">
        <SidebarItem label="Dashboard" to="/dashboard" />
        <SidebarItem label="Teams" to="/teams" />
        <SidebarItem label="Organisation" to="/organisation" />
        <SidebarItem label="Messages" to="/messages" />
        <SidebarItem label="Schedule" to="/schedule" />
      </nav>
    </aside>
  );
}