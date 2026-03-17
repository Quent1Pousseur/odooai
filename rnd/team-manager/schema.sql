-- OdooAI Team Manager — SQLite Schema
-- Persistent state for 48 agents across sessions

-- Agents — who they are and what they can do
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    department TEXT NOT NULL,
    disc_profile TEXT DEFAULT '',  -- D, I, S, C
    reports_to INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills — what each agent has learned (evolves over time)
CREATE TABLE IF NOT EXISTS agent_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    skill TEXT NOT NULL,
    source TEXT NOT NULL,  -- 'learning', 'rnd', 'task'
    sprint TEXT NOT NULL,
    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT DEFAULT ''
);

-- Current state — what each agent is doing RIGHT NOW
CREATE TABLE IF NOT EXISTS agent_state (
    agent_id INTEGER PRIMARY KEY REFERENCES agents(id),
    status TEXT NOT NULL DEFAULT 'available',  -- task, rnd, learning, available, blocked
    current_task TEXT DEFAULT '',
    current_project TEXT DEFAULT '',  -- R&D project name
    current_learning TEXT DEFAULT '',  -- learning subject
    last_deliverable TEXT DEFAULT '',
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- R&D Projects
CREATE TABLE IF NOT EXISTS rnd_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lead_agent_id INTEGER NOT NULL REFERENCES agents(id),
    status TEXT NOT NULL DEFAULT 'active',  -- active, pause, done, killed
    description TEXT DEFAULT '',
    code_path TEXT DEFAULT '',  -- rnd/nom-projet/
    doc_path TEXT DEFAULT '',   -- docs/rnd/NN-nom.md
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- R&D Project members
CREATE TABLE IF NOT EXISTS rnd_members (
    project_id INTEGER NOT NULL REFERENCES rnd_projects(id),
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    role TEXT DEFAULT 'contributor',  -- lead, contributor
    PRIMARY KEY (project_id, agent_id)
);

-- Learnings — history of all CRs
CREATE TABLE IF NOT EXISTS learnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    subject TEXT NOT NULL,
    sprint TEXT NOT NULL,
    file_path TEXT NOT NULL,  -- docs/learning/sprintN/NN-sujet.md
    key_takeaway TEXT DEFAULT '',
    recommendations TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- KPIs — measurable targets per agent
CREATE TABLE IF NOT EXISTS kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    metric TEXT NOT NULL,
    target TEXT NOT NULL,
    current_value TEXT DEFAULT '',
    sprint TEXT NOT NULL,
    measured_at TIMESTAMP
);

-- Session log — what happened each session
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    session_number INTEGER NOT NULL,
    sprint TEXT NOT NULL,
    summary TEXT DEFAULT '',
    agents_active INTEGER DEFAULT 0,
    agents_rnd INTEGER DEFAULT 0,
    agents_learning INTEGER DEFAULT 0,
    agents_idle INTEGER DEFAULT 0,
    commits INTEGER DEFAULT 0,
    tests INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_skills_agent ON agent_skills(agent_id);
CREATE INDEX IF NOT EXISTS idx_state_status ON agent_state(status);
CREATE INDEX IF NOT EXISTS idx_learnings_agent ON learnings(agent_id);
CREATE INDEX IF NOT EXISTS idx_learnings_sprint ON learnings(sprint);
CREATE INDEX IF NOT EXISTS idx_kpis_agent ON kpis(agent_id);
