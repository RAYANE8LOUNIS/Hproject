function SidebarItem({ label, active = false }) {
  return (
    <div className={`sidebar-item ${active ? "active" : ""}`}>
      <span className="sidebar-icon" />
      <span>{label}</span>
    </div>
  );
}

export default function Sidebar({ active }) {
  return (
    <aside className="sidebar">
      <div className="logo-wrap">
        <div className="logo-icon">≋</div>
        <div className="logo-text">Sky Portal</div>
      </div>

      <nav className="sidebar-nav">
        <SidebarItem label="Dashboard" active={active === "Dashboard"} />
        <SidebarItem label="Teams" active={active === "Teams"} />
        <SidebarItem label="Organisation" active={active === "Organisation"} />
        <SidebarItem label="Messages" active={active === "Messages"} />
        <SidebarItem label="Schedule" active={active === "Schedule"} />
      </nav>
    </aside>
  );
}