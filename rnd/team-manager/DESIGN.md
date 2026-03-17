# Team Manager — Design Document
## Le cerveau operationnel de l'entreprise

---

## Vision

Le CEO (fondateur) dit ce qu'il veut. Le systeme planifie, execute, mesure, et fait evoluer les equipes. Claude Code est le manager qui dispatche le travail via subagents.

---

## Entites

### 1. ENTREPRISE
```
company
  - name: "OdooAI"
  - vision: text
  - current_sprint: FK → sprint
  - created_at
```

### 2. AGENTS (les employes)
```
agents
  - id: 1-48
  - name: "CEO", "Backend Architect"...
  - role: description du poste
  - department: "C-Suite", "Engineering", "Business"...
  - disc_profile: "D", "I", "S", "C"
  - reports_to: FK → agent
  - seniority: "junior", "mid", "senior", "lead"
  - hired_at: date
  - is_active: bool

agent_skills  (evolue au fil du temps)
  - agent_id: FK
  - skill: "Python AST", "OpenTelemetry", "Odoo workflows"
  - level: "beginner", "intermediate", "advanced"
  - source: "learning", "rnd", "task"
  - acquired_at: date
  - sprint: dans quel sprint

agent_state  (etat ACTUEL — change a chaque session)
  - agent_id: FK
  - status: "task", "rnd", "learning", "available", "blocked"
  - current_activity: description
  - current_task_id: FK → task (nullable)
  - current_rnd_id: FK → rnd_project (nullable)
  - last_deliverable: text
  - last_active: timestamp
```

### 3. SPRINTS
```
sprints
  - id: auto
  - name: "Sprint 6 — Deploiement"
  - number: 6
  - status: "planning", "active", "review", "done"
  - start_date
  - end_date
  - goal: text
  - velocity_target: nombre de taches
  - created_at

sprint_metrics  (mesure a chaque session)
  - sprint_id: FK
  - session_date
  - tasks_done / tasks_total
  - tests_count
  - commits_count
  - learning_crs_count
  - wellbeing_score
```

### 4. TACHES
```
tasks
  - id: auto
  - title: "Auth JWT"
  - description: text
  - spec_id: "ODAI-SEC-003" (nullable)
  - sprint_id: FK → sprint
  - assigned_to: FK → agent (nullable)
  - status: "backlog", "todo", "in_progress", "review", "done", "blocked"
  - priority: "P0", "P1", "P2"
  - effort: "S", "M", "L"
  - blocker: text (nullable)
  - depends_on: FK → task (nullable)
  - github_issue: "#49" (nullable)
  - created_at
  - started_at
  - completed_at
  - eta_hours: float (nullable)

task_history  (chaque changement est trace)
  - task_id: FK
  - field_changed: "status", "sprint_id", "assigned_to"
  - old_value
  - new_value
  - changed_at
  - reason: text
```

### 5. PROJETS R&D
```
rnd_projects
  - id: auto
  - name: "SEO Content Generator"
  - description: text
  - lead_agent_id: FK → agent
  - status: "proposed", "active", "pause", "done", "killed"
  - code_path: "rnd/seo-content-generator/"
  - doc_path: "docs/rnd/37-seo-content-generator.md"
  - mvp_description: text
  - budget_tokens: int (max tokens LLM autorises)
  - created_at
  - updated_at

rnd_members
  - project_id: FK
  - agent_id: FK
  - role: "lead", "contributor"
  - joined_at

rnd_progress  (avancement par session)
  - project_id: FK
  - session_date
  - description: "Cree generate.py + 5 articles"
  - files_changed: int
  - lines_added: int
```

### 6. FORMATIONS (Learnings)
```
learnings
  - id: auto
  - agent_id: FK
  - subject: "Python AST module"
  - sprint: "sprint5"
  - file_path: "docs/learning/sprint5/20-junior-backend-ast-python.md"
  - key_takeaways: text (resume des points cles)
  - recommendations: text (ce que l'agent recommande)
  - applicable_to: text (comment ca s'applique au projet)
  - duration_hours: float
  - created_at
```

### 7. PLANS D'ONBOARDING
```
onboarding_plans
  - id: auto
  - department: "Engineering Backend"
  - steps: JSON [
      {"order": 1, "task": "Lire CLAUDE.md + PROCESS.md", "duration": "30min"},
      {"order": 2, "task": "Lire les 3 specs du domaine", "duration": "1h"},
      {"order": 3, "task": "Faire un test simple", "duration": "2h"},
      {"order": 4, "task": "Pair programming avec le lead", "duration": "4h"},
      {"order": 5, "task": "Premiere tache solo (S)", "duration": "1 jour"}
    ]
  - created_at

onboarding_progress
  - agent_id: FK
  - plan_id: FK
  - current_step: int
  - completed_at: timestamp (nullable)
```

### 8. KPIs
```
kpi_definitions
  - id: auto
  - agent_id: FK
  - metric: "test_coverage"
  - target: "> 80%"
  - measurement: "make check → coverage report"

kpi_measurements
  - kpi_id: FK
  - sprint: "sprint5"
  - value: "78%"
  - status: "on_track", "at_risk", "missed"
  - measured_at
```

### 9. COMMUNICATION
```
decisions
  - id: auto
  - title: "Pivot buddy mode"
  - description: text
  - decided_by: FK → agent
  - sprint: text
  - impact: text
  - created_at

meetings
  - id: auto
  - type: "session", "retro", "kickoff", "team_building"
  - date
  - sprint
  - file_path: "docs/meetings/sessions/..."
  - summary: text
  - agents_present: int
  - challenges_count: int
```

### 10. WELLBEING
```
wellbeing_surveys
  - id: auto
  - sprint
  - date
  - overall_score: float

wellbeing_scores
  - survey_id: FK
  - agent_id: FK
  - charge: int (1-10)
  - motivation: int (1-10)
  - alignment: int (1-10)
  - collaboration: int (1-10)
```

---

## Commandes CLI

### Session management
```bash
team.py session-start          # Contexte complet + alertes
team.py session-end            # Sauvegarde + met a jour SESSION_STATE.md
```

### Agents
```bash
team.py agents                 # Liste tous les agents + status
team.py agent 37               # Detail complet d'un agent
team.py agent 37 --history     # Evolution au fil du temps
team.py agent 37 --skills      # Competences acquises
team.py assign 37 --task 42    # Assigner une tache
team.py assign 37 --rnd 2      # Assigner a un projet R&D
team.py available              # Qui est disponible ?
```

### Sprints & Taches
```bash
team.py sprint                 # Sprint actuel + status
team.py sprint --create "Sprint 7" --goal "Multi-tenant"
team.py tasks                  # Toutes les taches du sprint
team.py task 42                # Detail d'une tache
team.py task 42 --status done  # Changer le status
team.py task 42 --sprint 7     # Deplacer au sprint 7
team.py eta                    # ETA du sprint actuel
team.py velocity               # Velocity (taches/session)
team.py burndown               # Burndown chart (texte)
```

### R&D
```bash
team.py rnd                    # Projets R&D actifs
team.py rnd 2 --progress "Ajoute le multi-module"
team.py rnd --propose "Bot Discord" --lead 47
```

### Formation
```bash
team.py learn 20 --subject "Python AST" --sprint 5
team.py learnings              # Tous les learnings du sprint
team.py skills 38              # Competences de l'agent 38
team.py skills --search "OpenTelemetry"  # Qui connait ca ?
```

### KPIs & Wellbeing
```bash
team.py kpis                   # KPIs du sprint
team.py kpis 13                # KPIs du QA Lead
team.py wellbeing              # Score wellbeing actuel
```

### Onboarding
```bash
team.py onboard 49 --department "Engineering Backend"
team.py onboard 49 --step 3    # Marquer l'etape 3 comme faite
```

### ETA & Reporting
```bash
team.py status                 # Resume complet (pour Claude Code au demarrage)
team.py report                 # Rapport de fin de session (pour le fondateur)
```

---

## Interaction Claude Code

### Demarrage de session
```
Claude Code lit CLAUDE.md → voit "Protocole de demarrage"
  → execute `python team.py session-start`
  → recoit : sprint actuel, taches, agents dispos, alertes
  → fait le daily meeting avec ces infos
```

### Pendant la session
```
Fondateur : "Lance les taches du sprint"
  → Claude Code : `python team.py tasks --status todo`
  → Recoit la liste des taches
  → Lance des subagents pour chaque tache
  → `python team.py task 42 --status in_progress`

Fondateur : "Ou en est le sprint ?"
  → Claude Code : `python team.py eta`
  → "12/20 taches done, velocity 8/session, ETA 1 session"

Fondateur : "Qui peut bosser sur le dashboard ?"
  → Claude Code : `python team.py skills --search "frontend"`
  → "Agent 21 (Frontend Eng), Agent 39 (Mobile), Agent 27 (UX)"
```

### Fin de session
```
Claude Code : `python team.py session-end --commits 15 --tests 230`
  → DB mise a jour
  → SESSION_STATE.md regenere automatiquement
  → Rapport de session genere
```

---

## MVP — Ce qu'on code en premier

Phase 1 : Schema + seed data (48 agents)
Phase 2 : Commandes de base (session-start, agents, status, assign)
Phase 3 : Sprint & tasks (create, move, eta)
Phase 4 : Learnings & skills (learn, skills)
Phase 5 : session-end (rapport + SESSION_STATE.md auto)
