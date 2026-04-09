import { useState, useRef, useEffect } from "react";

export default function Header({ title }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  function handleLogout() {
    alert("Logout functionality can be connected later.");
    setMenuOpen(false);
  }

  return (
    <header className="topbar">
      <h1>{title}</h1>

      <div className="topbar-right">
        <button className="circle-btn" type="button">
          ◌
        </button>

        <div className="profile-menu-wrap" ref={menuRef}>
          <button
            className="profile-pill profile-trigger"
            type="button"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <div className="profile-avatar" />
            <span>User</span>
            <span className="chevron">˅</span>
          </button>

          {menuOpen && (
            <div className="profile-dropdown">
              <button
                className="profile-dropdown-item"
                type="button"
                onClick={() => setMenuOpen(false)}
              >
                View Profile
              </button>

              <button
                className="profile-dropdown-item"
                type="button"
                onClick={() => setMenuOpen(false)}
              >
                Settings
              </button>

              <button
                className="profile-dropdown-item danger-item"
                type="button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}