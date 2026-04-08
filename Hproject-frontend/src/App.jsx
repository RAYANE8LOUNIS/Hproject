import { useState } from "react";
import "./index.css";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import TeamDirectory from "./pages/Teams/TeamDirectory";
import TeamProfile from "./pages/Teams/TeamProfile";

export default function App() {
  const [currentPage, setCurrentPage] = useState("teams");
  const [selectedTeam, setSelectedTeam] = useState(null);

  const handleOpenTeam = (team) => {
    setSelectedTeam(team);
    setCurrentPage("team-profile");
  };

  const handleBackToTeams = () => {
    setSelectedTeam(null);
    setCurrentPage("teams");
  };

  return (
    <div className="app-shell">
      <Sidebar active="Teams" />

      {currentPage === "teams" && (
        <main className="main-content">
          <Header title="Team Directory" />
          <TeamDirectory onOpenTeam={handleOpenTeam} />
        </main>
      )}

      {currentPage === "team-profile" && selectedTeam && (
        <main className="main-content">
          <Header title={selectedTeam.name} />
          <TeamProfile team={selectedTeam} onBack={handleBackToTeams} />
        </main>
      )}
    </div>
  );
}