import "./index.css";
import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import TeamDirectory from "./pages/Teams/TeamDirectory";
import TeamProfile from "./pages/Teams/TeamProfile";

function TeamsLayout({ children, title }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <Header title={title} />
        {children}
      </main>
    </div>
  );
}

function PlaceholderPage({ title }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <Header title={title} />
        <div className="team-card">
          <h3>{title}</h3>
          <p className="muted-text">
            This section will be connected when your teammate finishes it.
          </p>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/teams" replace />} />

      <Route
        path="/teams"
        element={
          <TeamsLayout title="Team Directory">
            <TeamDirectory />
          </TeamsLayout>
        }
      />

      <Route
        path="/teams/:teamId"
        element={
          <TeamsLayout title="Team Profile">
            <TeamProfile />
          </TeamsLayout>
        }
      />

      <Route path="/dashboard" element={<PlaceholderPage title="Dashboard" />} />
      <Route path="/organisation" element={<PlaceholderPage title="Organisation" />} />
      <Route path="/messages" element={<PlaceholderPage title="Messages" />} />
      <Route path="/schedule" element={<PlaceholderPage title="Schedule" />} />
    </Routes>
  );
}