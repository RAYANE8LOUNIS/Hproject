import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

export default function TeamProfile() {
  const navigate = useNavigate();
  const { teamId } = useParams();

  const [activeTab, setActiveTab] = useState("Overview");
  const [teamDetail, setTeamDetail] = useState(null);

  const tabs = ["Overview", "Members", "Repositories", "Dependencies"];

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/teams/api/teams/${teamId}/`)
      .then((res) => res.json())
      .then((data) => setTeamDetail(data))
      .catch((err) => console.error("Error fetching team detail:", err));
  }, [teamId]);

  if (!teamDetail) {
    return <div className="team-card">Loading team profile...</div>;
  }

  const emailHref = teamDetail.email
    ? `mailto:${teamDetail.email}?subject=${encodeURIComponent(`Message for ${teamDetail.name}`)}`
    : null;

  return (
    <>
      <div className="profile-actions">
        <button className="icon-btn" onClick={() => navigate("/teams")}>
          ←
        </button>
      </div>

      <section className="profile-hero-card">
        <div className="profile-hero-left">
          <div className="profile-avatar-large" />
          <div>
            <h2 className="profile-title">{teamDetail.name}</h2>
            <p className="profile-subtitle">{teamDetail.manager}</p>
            <span className="status-badge">{teamDetail.status}</span>
          </div>
        </div>

        <div className="profile-buttons">
          {emailHref ? (
            <a href={emailHref} className="secondary-btn link-btn">
              Email Team
            </a>
          ) : (
            <button className="secondary-btn" disabled>
              No Email
            </button>
          )}

          <a
            href={`http://127.0.0.1:8000/teams/${teamId}/schedule/`}
            className="primary-btn link-btn"
            target="_blank"
            rel="noreferrer"
          >
            Schedule Meeting
          </a>
        </div>
      </section>

      <section className="tabs-row">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`tab-btn ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </section>

      {activeTab === "Overview" && (
        <div className="profile-layout">
          <div className="profile-main-column">
            <div className="team-card">
              <h3>Overview</h3>
              <p className="muted-text">
                This section gives a general summary of the team and its role
                within the organisation.
              </p>

              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Team Name</span>
                  <span className="info-value">{teamDetail.name}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Manager</span>
                  <span className="info-value">{teamDetail.manager}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Department</span>
                  <span className="info-value">{teamDetail.department}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Team Type</span>
                  <span className="info-value">{teamDetail.team_type}</span>
                </div>
              </div>
            </div>

            <div className="team-card">
              <h3>Description</h3>
              <p className="muted-text">
                {teamDetail.description || "No description available."}
              </p>
            </div>
          </div>

          <div className="profile-side-column">
            <div className="team-card">
              <h3>Quick Stats</h3>
              <div className="stats-stack">
                <div className="stat-row">
                  <span>Members</span>
                  <strong>{teamDetail.members_count}</strong>
                </div>
                <div className="stat-row">
                  <span>Repositories</span>
                  <strong>{teamDetail.repositories_count}</strong>
                </div>
              </div>
            </div>

            <div className="team-card">
              <h3>Skills</h3>
              <div className="skills-wrap">
                <span className="pill-tag">{teamDetail.team_type || "No Team Type"}</span>
                <span className="pill-tag">{teamDetail.department || "No Department"}</span>
                <span className="pill-tag">{teamDetail.status || "Unknown Status"}</span>
              </div>
            </div>

            <div className="team-card">
              <h3>Contact</h3>
              <p className="muted-text">
                <strong>Email:</strong> {teamDetail.email || "No email available"}
              </p>
              <p className="muted-text">
                <strong>Slack:</strong> {teamDetail.slack_channel || "No slack channel available"}
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === "Members" && (
        <div className="team-card">
          <h3>Members</h3>
          <div className="list-card">
            {teamDetail.members.length > 0 ? (
              teamDetail.members.map((member) => (
                <div key={member.id} className="list-row">
                  <div className="list-avatar" />
                  <div>
                    <strong>{member.username}</strong>
                    <p className="muted-text">Team Member</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="muted-text">No members yet.</p>
            )}
          </div>
        </div>
      )}

      {activeTab === "Repositories" && (
        <div className="team-card">
          <h3>Repositories</h3>
          {teamDetail.code_repository ? (
            <div className="repo-card">
              <strong>Main Repository</strong>
              <p className="muted-text">{teamDetail.code_repository}</p>
              <a
                href={teamDetail.code_repository}
                target="_blank"
                rel="noreferrer"
                className="secondary-btn link-btn small-link-btn"
              >
                Open Repository
              </a>
            </div>
          ) : (
            <p className="muted-text">No repositories yet.</p>
          )}
        </div>
      )}

      {activeTab === "Dependencies" && (
        <div className="dependencies-grid">
          <div className="team-card">
            <h3>Upstream Dependencies</h3>
            {teamDetail.upstream_dependencies.length > 0 ? (
              teamDetail.upstream_dependencies.map((dep) => (
                <div key={dep.id} className="dependency-box">
                  <strong>{dep.team_name}</strong>
                  <p className="muted-text">
                    {dep.description || "No description available."}
                  </p>
                </div>
              ))
            ) : (
              <p className="muted-text">No upstream dependencies.</p>
            )}
          </div>

          <div className="team-card">
            <h3>Downstream Dependencies</h3>
            {teamDetail.downstream_dependencies.length > 0 ? (
              teamDetail.downstream_dependencies.map((dep) => (
                <div key={dep.id} className="dependency-box">
                  <strong>{dep.team_name}</strong>
                  <p className="muted-text">
                    {dep.description || "No description available."}
                  </p>
                </div>
              ))
            ) : (
              <p className="muted-text">No downstream dependencies.</p>
            )}
          </div>
        </div>
      )}
    </>
  );
}