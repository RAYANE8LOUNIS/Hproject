import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

function AvatarGroup() {
  return (
    <div className="avatar-group">
      <div className="mini-avatar" />
      <div className="mini-avatar overlap" />
      <div className="mini-avatar overlap" />
    </div>
  );
}

function TeamCard({ team, onOpenTeam }) {
  return (
    <div
      className="team-card clickable-card"
      onClick={() => onOpenTeam(team.id)}
    >
      <div className="team-card-top">
        <div>
          <h3>{team.name}</h3>
          <p className="manager-name">{team.manager}</p>
        </div>
        <span className="status-badge">{team.status}</span>
      </div>

      <div className="team-stats">
        <span>{team.members} Members</span>
        <span>{team.repositories} Repositories</span>
      </div>

      <div className="divider" />

      <div className="team-card-bottom">
        <AvatarGroup />

        <div className="card-actions">
          <button
            className="icon-btn"
            onClick={(e) => e.stopPropagation()}
          >
            ⋮
          </button>
        </div>
      </div>
    </div>
  );
}

export default function TeamDirectory() {
  const navigate = useNavigate();

  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All Departments");
  const [sortBy, setSortBy] = useState("Sort by Name");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams/api/teams/")
      .then((res) => res.json())
      .then((data) => {
        setTeams(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching teams:", err);
        setLoading(false);
      });
  }, []);

  const filteredTeams = useMemo(() => {
    let result = [...teams];

    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (team) =>
          team.name.toLowerCase().includes(q) ||
          team.manager.toLowerCase().includes(q) ||
          team.department.toLowerCase().includes(q)
      );
    }

    if (departmentFilter !== "All Departments") {
      result = result.filter((team) => team.department === departmentFilter);
    }

    if (sortBy === "Sort by Name") {
      result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === "Sort by Members") {
      result.sort((a, b) => b.members - a.members);
    } else if (sortBy === "Sort by Repositories") {
      result.sort((a, b) => b.repositories - a.repositories);
    }

    return result;
  }, [teams, search, departmentFilter, sortBy]);

  const departmentOptions = [
    "All Departments",
    ...new Set(teams.map((team) => team.department).filter(Boolean)),
  ];

  return (
    <>
      <section className="filters-row">
        <div className="search-box">
          <span className="search-icon">⌕</span>
          <input
            type="text"
            placeholder="Search teams..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          className="filter-select"
          value={departmentFilter}
          onChange={(e) => setDepartmentFilter(e.target.value)}
        >
          {departmentOptions.map((option) => (
            <option key={option}>{option}</option>
          ))}
        </select>

        <select
          className="filter-select"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option>Sort by Name</option>
          <option>Sort by Members</option>
          <option>Sort by Repositories</option>
        </select>
      </section>

      {loading ? (
        <div className="team-card empty-state-card">
          <h3>Loading teams...</h3>
          <p className="muted-text">Please wait while the team directory loads.</p>
        </div>
      ) : filteredTeams.length === 0 ? (
        <div className="team-card empty-state-card">
          <h3>No teams found</h3>
          <p className="muted-text">
            Try changing the search or filter options.
          </p>
        </div>
      ) : (
        <section className="cards-grid">
          {filteredTeams.map((team) => (
            <TeamCard
              key={team.id}
              team={team}
              onOpenTeam={(id) => navigate(`/teams/${id}`)}
            />
          ))}
        </section>
      )}
    </>
  );
}