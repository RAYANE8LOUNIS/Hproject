export default function Header({ title }) {
  return (
    <header className="topbar">
      <h1>{title}</h1>

      <div className="topbar-right">
        <button className="circle-btn">◌</button>

        <div className="profile-pill">
          <div className="profile-avatar" />
          <span>User</span>
          <span className="chevron">⌄</span>
        </div>
      </div>
    </header>
  );
}