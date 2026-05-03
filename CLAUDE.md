# DivineSide — Claude Code Context

This file gives Claude Code full context on DivineSide, DivineCore, the team, the tech stack, the business model, and the current state of the build. Read this before touching anything.


## 1. COMPANY OVERVIEW

Company name: DivineSide  
Type: AI Operating System (AI OS) Agency  
One-liner: "DivineSide turns businesses into systems."  
Stage: Early — building, testing, getting first clients, finding distribution

Core philosophy:
- Traditional business: people execute, tools assist
- DivineSide model: systems execute, people supervise
- The shift: from doing work to designing systems

DivineSide is not an automation agency. We do not build chatbots and call them AI. We build fully autonomous operating systems that run entire functions of a business end-to-end. The machine executes. Humans supervise.


## 2. BUSINESS MODEL

**Stage 1 — Custom AI OS Builds (Current)**  
We build fully autonomous operating systems for client businesses. Each build runs an entire department or business function. Niche-agnostic for now — experimenting across industries to find patterns. Each build = cash flow + R&D simultaneously.

Running in parallel: commoditised solutions (chatbots, simple automations, SMS flows, lead capture) that feed the startup financially while deeper AI OS work develops.

**Stage 2 — GaaS: Agentic as a Service (Future)**  
After enough custom builds and niche discovery, we productise. Autonomous OS delivered as a subscription. What SaaS was 15 years ago — except instead of a tool, the client gets a system that runs a business function entirely. Product name not yet finalised. We earn our way here one build at a time.

DivineCore is the name for DivineSide's internal system only. The external product name is TBD.


## 3. DIVINECORE — INTERNAL BUSINESS OS

DivineCore is DivineSide's own Business Operating System. It is:
- NOT a product we sell
- NOT marketed externally
- The internal proof of concept — runs the agency itself
- The architecture template for all client builds

Every system we build for clients is derived from architecture first proven in DivineCore.

**Primary Interface**  
Discord — real-time, bot-native, structured by channel as department. Agents live as Discord bots. Each module has its own channel. Admin commands go through a private #pulse channel.

Discord Server: DivineSide | Server ID: 1489255611857371266

DivineCore channels:
- #branding — ID: 1495654627322892319
- #sales-and-outreach — ID: 1495654885218189392
- #recruitment-and-networking — ID: 1495655231013519422
- #operations — ID: 1495655877900763186
- #pulse — private admin channel


## 4. TECH STACK

| Layer | Tool | Notes |
|-------|------|-------|
| Interface | Discord | Primary operating environment |
| Automation/Workflow | n8n | Self-hosted on Hostinger VPS |
| Development | Claude Code | Primary and increasingly dominant dev tool |
| AI Models | Anthropic (Claude), OpenAI (GPT-4o mini) | Via OpenRouter as fallback |
| Database (structured) | Airtable | Knowledge bases, task tracking, CRM |
| Database (vector) | Supabase + pgvector | Semantic search for working examples |
| Embeddings | OpenAI text-embedding-3-small | For Supabase vector store |
| Middleware | Node.js (discord.js) | Discord → n8n webhook bridge |
| VPS | Hostinger | srv1445995.hstgr.cloud / IP: 187.124.96.99 |
| Process Manager | PM2 | Keeps middleware alive, survives reboots |
| Reverse Proxy | Nginx | HTTPS routing on VPS |
| Future Interface | Proprietary app (TBD) | Replaces Discord when DivineSide launches publicly |

**n8n Instance**  
URL: https://n8n.srv1445995.hstgr.cloud  
Hosted on Hostinger VPS. All workflows live here.

**Discord Middleware**  
Location on VPS: /root/discord-middleware/index.js  
Forwards Discord messages to n8n webhooks  
Server webhook: 16202f28-06f5-4d4a-8060-97dcd9986c3b  
DM webhook: d0ecdaad-f267-4fd5-8719-36ffe007067f  
PM2 commands: pm2 start/restart/logs discord-middleware

**Code Stack Direction**  
Claude Code is the primary build tool going forward. Python scripts for agents, tools, and system logic live in this GitHub repo. n8n handles orchestration and workflow triggers. Claude Code handles everything that requires real code — custom logic, API integrations, agent tool definitions, data processing.


## 5. THE RESEARCH PHILOSOPHY — THE CORE MOAT

The product is not built around tools. It is built around research.

Each DivineCore module is fed the encoded knowledge, frameworks, and mental models of the best practitioners in that domain. This is the competitive defensibility. No enterprise tool can replicate this because they build features — we build expertise into the system.

When the underlying tools change (and they will), the research and domain intelligence remains.

Current knowledge bases:

| Module | Source | Format |
|--------|--------|--------|
| Branding OS | Kallaway (YouTube creator — best research on content creation) | Airtable (exact retrieval) + Supabase (semantic search) |
| Sales OS | Alex Hormozi — $100M Offers + $100M Leads books | Airtable (structured frameworks) |

Research workflow: watch source material → Tactiq transcription → Glasp highlights → paste into Claude Research project → extract structured lessons → enter into Airtable.


## 6. THE FIVE MODULES

### Module 1 — Branding OS (Creative Intelligence)
Status: In development (IMAGYN active, others in build)  
Priority: Highest strategic value

Full content pipeline from idea to publish-ready output. Five named agents:

| Agent | Role |
|-------|------|
| IMAGYN | Idea generation — pulls from Kallaway KB + working examples |
| LYRA | Script writing — emotional resonance, story structure |
| MONTAGE | Editing brief — b-roll, pacing, music, transitions |
| FORGE | Visual prompt generation for diffusion models (Midjourney, Runway, Flux) |
| VIGIL | Performance feedback loop — Instagram Graph API + YouTube Analytics |

Knowledge base architecture:
- **Airtable (Core Knowledge Base):** Kallaway's lessons. Fields: Title, Category, Core Lesson, Full Explanation, Content Attributes, Content Types, Source URL, Notes. 51+ entries. Exact retrieval.
- **Supabase (Working Examples):** Real high-performing content pieces. Embedded via OpenAI text-embedding-3-small. pgvector semantic search. Finds examples by meaning, not keyword.

Content Attributes (Kallaway framework): TAM Resonance, Idea Explosivity, Emotional Magnitude, Novelty, Speed to Value, Curiosity Amplitude, Absorption Rate, Rehook Rate, Stickiness

Automation philosophy on cost: Where API calls to generation models (video, image) are prohibitively expensive, the system generates the prompt and a human executes manually. FORGE outputs prompts — human runs them. Ops OS alerts the human when a prompt is ready and time-sensitive.

Platforms: YouTube + Instagram (primary), LinkedIn + Reddit (secondary)  
Target: Minimum one piece of content per day


### Module 2 — Sales OS (Revenue System)
Status: In planning/early build

Manages the full sales pipeline AND does active outbound. This is not a passive CRM — it initiates contact, sends messages, and runs follow-up sequences. Eventually makes outbound calls.

Knowledge base: Alex Hormozi's $100M series — full frameworks, money models, offer construction, lead conversion. Applied directly inside agent reasoning layer.

Capabilities:
- Lead storage + categorisation (hot/warm/cold)
- AI-generated personalised follow-ups
- Pipeline tracking: Lead → Contacted → Interested → Closed
- Conversation tracking (last message, next action)
- Deal tracking + client memory
- Outbound: DMs, LinkedIn, WhatsApp, calls (when budget allows)

Agents: Lead Agent, Follow-up Agent, Deal Agent


### Module 3 — Ops OS (Execution System)
Status: Planning

The manual automation layer. Highest-leverage function: real-time gap detection. When any pipeline reaches a step requiring manual intervention, Ops OS detects it and immediately alerts the right person via message or call.

Core concept: No system is 100% automated. There are always gaps — API cost too high, human judgment required, infrastructure not built yet. Ops OS ensures these gaps never become blockers. It identifies them, escalates them, and keeps the pipeline moving.

Example: Branding OS generates a visual prompt. Direct API call to generation model costs 10x more than running it manually. System generates the prompt. Ops OS immediately messages whoever is available: "Prompt ready, needs execution within X minutes." Human does one mechanical step. Pipeline continues.

Additional capabilities: Task assignment, deadline tracking, responsibility mapping, workflow monitoring.

Agents: Task Agent, Reminder Agent, Monitoring Agent


### Module 4 — Pulse (Alert + Awareness System)
Status: Active and published

The urgency and accountability layer. Lives across ALL module channels simultaneously.

Bot name: Pulse (APP)  
Model: GPT-4o mini via OpenRouter  
Memory: Postgres Chat Memory (session key = username)  
Addresses Mayank as: "Sir"

Functions:
- Morning digest at 03:30 IST — active tasks per channel
- Progressive reminders at 1/3 and 2/3 of deadline window
- Breach detection — deadline passed + status ≠ done → immediate alert
- Admin commands via #pulse (private channel only)
- Responds only when tagged in channels

Airtable task database: DivineCore base, Task table  
Fields: Task, Assignee, Channel, Status (in-progress/done), Priority (high/medium/low), Deadline, Created By, Discord Message ID, Notes, Deadline reached?

n8n workflows:
- Pulse Agent: https://n8n.srv1445995.hstgr.cloud/workflow/veDyMBIC6uCoULYb
- Reminder Sequence: https://n8n.srv1445995.hstgr.cloud/workflow/lpkxm5wGHXJF53ru
- Receive Messages (Server): webhook 16202f28-06f5-4d4a-8060-97dcd9986c3b
- Receive Messages (DM): webhook d0ecdaad-f267-4fd5-8719-36ffe007067f


### Module 5 — Networking & Recruitment OS
Status: In build

Automates the exact networking and recruiting behaviour Mayank does manually — deployed at scale across every relevant platform simultaneously.

Philosophy: Clones of manual behaviour. The system does not do something different from what a human would do — it does exactly the same thing, everywhere, all the time.

Current capabilities:
- Bots that auto-comment on relevant YouTube videos (recruiting + networking)
- Discord bots deployed inside relevant servers
- Outreach drafts generated per platform and context

Expansion targets: LinkedIn, Reddit, Skool communities, Discord servers, YouTube


## 7. THE TEAM

| Name | Role | Status | Notes |
|------|------|--------|-------|
| Mayank Rawat | CEO, Engineering, Video Content | Active | Owns product vision, system architecture, all video content. Discord: mayank082527 |
| Shubham | Co-Founder, Research & Ops | Active | Owns Kallaway knowledge base build and operational support |
| Pang (彭毅和) | Developer + Marketing | New — evaluating as co-founder | CS at Wuhan University, China. Strong technical + marketing background. |
| William | Sales, Written Content | Team (being tested) | LinkedIn outreach, DMs, written content formats |
| Anish | Lead Developer | Team (being tested) | Development execution |


## 8. DISTRIBUTION — CURRENT STATE

Primary: Mayank's personal network. Warm relationships, direct conversations, trusted introductions. Highest-conversion channel at this stage.

Secondary: Direct outreach — team executing manually via DMs, LinkedIn, targeted conversations. Cold calling being introduced shortly.

Sales OS will handle outreach autonomously as it matures — the team sets strategy, the system executes volume.

Long-term engine: Brand. Building in public across YouTube and Instagram. Almost nobody is building AI OS systems at this level AND documenting it publicly. That is the positioning edge. Once Branding OS is fully operational, content production is largely automated — distribution becomes self-sustaining.


## 9. CONTENT & SOCIAL STRATEGY

Platforms: YouTube + Instagram (primary), LinkedIn + Reddit (secondary)  
Cadence: Minimum one piece of content per day  
Content types: Long-form video, short-form video, carousels, tweets/text posts, images

Content categories:
- Journey — what we're building, what's working, what isn't. Raw and honest.
- Lessons and insights — practical, not just inspirational
- DivineSide as AI OS agency — behind-the-scenes builds
- Client work — case studies, testimonials, results
- Business lessons — for founders and entrepreneurs

Positioning: We are not competing with generic creators. We are attracting founders, entrepreneurs, and operators who understand AI is infrastructure, not a tool. Build in public. Show wins and failures. Teach as we learn.

Monetisation layers:
- Custom AI OS builds (primary lead gen from content)
- Brand deals + advertisements
- Community + premium access (free community → paid upsells)
- Coaching + consulting (high ticket, accelerator-style)
- One-on-one coaching


## 10. ACCOUNTS & CREDENTIALS REFERENCE

Do not store passwords or API keys in this file. Reference only.

- n8n: https://n8n.srv1445995.hstgr.cloud
- VPS: srv1445995.hstgr.cloud | IP: 187.124.96.99
- Airtable base: DivineCore
- Primary email (old): mayankrawat000072@gmail.com


## 11. REPOSITORY STRUCTURE CONVENTIONS

```
DivineSide/
├── CLAUDE.md                  ← This file. Always keep updated.
├── README.md                  ← Public-facing repo overview
├── .env.example               ← Environment variable template (no real values)
├── branding-os/               ← Module 1: Creative Intelligence
│   ├── agents/                ← Agent definitions and system prompts
│   ├── knowledge-base/        ← KB management scripts
│   ├── workflows/             ← n8n workflow exports (JSON)
│   └── README.md
├── sales-os/                  ← Module 2: Revenue System
│   ├── agents/
│   ├── workflows/
│   └── README.md
├── ops-os/                    ← Module 3: Execution System
│   ├── agents/
│   ├── workflows/
│   └── README.md
├── pulse/                     ← Module 4: Alert + Awareness
│   ├── agents/
│   ├── workflows/
│   └── README.md
├── networking-os/             ← Module 5: Networking & Recruitment
│   ├── agents/
│   ├── bots/
│   ├── workflows/
│   └── README.md
├── infrastructure/            ← VPS, middleware, Discord bot, nginx configs
│   ├── discord-middleware/
│   └── README.md
└── shared/                    ← Shared resources used across modules
    ├── context/               ← Cross-module identity context (business-info, mayank, pang, voice, strategy, audience, linkedin-playbook). Every writing agent loads from here.
    ├── utils/                 ← Shared utilities, base classes, common tools
    └── README.md
```


## 12. WORKING CONVENTIONS

- **Claude Code is the primary development tool.** Use it for all Python, scripting, agent logic, and complex custom builds.
- **n8n handles orchestration.** Triggers, routing, inter-agent handoffs, scheduled workflows. Export workflow JSONs to /module/workflows/ for version control.
- **One agent, one job.** Never combine responsibilities into a single agent. Separate agents = less hallucination, lower API cost, more precise outputs, faster execution.
- **Manual first, automate second.** Never automate a workflow that hasn't been run manually enough to understand all edge cases. Document the manual process first, then build from it.
- **Research drives architecture.** Before building any agent, define its knowledge base source. The agent is only as good as the research fed into it.
- **Mayank assigns tasks. System tracks everything after.** Task assignment is always manual and intentional. Automation handles reminders, tracking, and escalation.
- **Commit workflow exports.** Every time an n8n workflow is updated, export the JSON and commit it to the relevant module folder.
- **Writing agents load from `shared/context/`.** Any agent producing copy aimed at humans (sales emails, LinkedIn posts, YouTube scripts, DMs, follow-ups) MUST pull from `shared/context/` in addition to its domain KB. Brand-level files: `business-info.md`, `voice.md`, `strategy.md`, `audience.md`. Per-person persona files: `mayank.md`, `pang.md` (load whichever team member the content is voiced as). Channel-specific tactical playbooks: `linkedin-playbook.md` (more to come). CLAUDE.md is for system architecture; `shared/context/` is for brand voice. Don't duplicate identity content into module folders — reference it.


## 13. DIVINECORE V2 — CODE-FIRST RUNTIME (IN BUILD)

Parallel track to the n8n-orchestrated stack. `divinecore-v2/` is the code-first runtime that will eventually replace n8n for agent execution — Python services owned end-to-end in this repo, deployable as containers.

### Foundation (commit `3c03553`)

Stack: **FastAPI API + Celery worker + Celery Beat scheduler + Redis broker**, all in Docker Compose.

```
divinecore-v2/
├── api/                       ← FastAPI service
│   ├── main.py                ← Routes + Celery client (send_task / AsyncResult)
│   ├── requirements.txt
│   └── Dockerfile
├── worker/                    ← Celery worker + beat (shares same image)
│   ├── celery_app.py          ← Celery config + beat_schedule
│   ├── tasks.py               ← echo, heartbeat
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml         ← redis + api + worker + beat
└── .dockerignore
```

Services in compose:
- `redis` — `redis:7-alpine`, exposes 6379
- `api` — FastAPI on `:8000`, talks to Celery via `REDIS_URL`
- `worker` — Celery worker, processes tasks from Redis
- `beat` — Celery Beat, runs scheduled tasks (currently `tasks.heartbeat` every 30s)

Endpoints today:
- `GET /` — health
- `POST /tasks/echo` — submit a task, returns `task_id`
- `GET /tasks/{task_id}` — poll status + result

Run locally: `cd divinecore-v2 && docker compose up --build`

### CI/CD Workflow (commit `3573662`)

File: `.github/workflows/divinecore-v2-ci.yml`

Triggers: push/PR to `main` (path-filtered to `divinecore-v2/**` and the workflow file itself) + `workflow_dispatch`.

**Build & push job** (matrix: `api`, `worker`):
- Runs both components in parallel via matrix strategy
- Uses `docker/setup-buildx-action@v3` + `docker/build-push-action@v6`
- Pushes to `ghcr.io/onebox69/aios-divinecore/{api,worker}`
- Tags: `:latest` (main only), `:sha-<short>`, `:<branch>`
- GHA cache scoped per component (`cache-from/to` with `scope=${name}`) — fast incremental rebuilds
- PRs are build-only (no push to GHCR, no Discord ping) — gated on `github.event_name != 'pull_request'`

**Notify job:**
- Runs after `build-and-push`, only on `push` events
- Uses `sarisia/actions-status-discord@v1`
- Posts status embed (success/failure) to `#deploys` via `DISCORD_WEBHOOK_URL` secret
- Embed includes branch + commit message

Required GitHub secrets:
- `GITHUB_TOKEN` — provided automatically, used for GHCR auth
- `DISCORD_WEBHOOK_URL` — webhook for `#deploys` channel (must be set in repo settings)

Permissions on the build job: `contents: read`, `packages: write` (needed to push to GHCR).

### Phase 2 — Pending

SSH-deploy from CI to the Hostinger VPS (`srv1445995.hstgr.cloud`). Blocked on VPS access. Once unblocked: pull tagged image on VPS, swap container, health-check.


## 14. CLAUDE CODE SLASH COMMANDS

Project-scoped slash commands live in `.claude/commands/` and are version-controlled. Each `.md` file becomes an invocable command (e.g. `prime.md` → `/prime`).

| Command | Purpose |
|---------|---------|
| `/prime` | Load full DivineCore context at session start. Reads `CLAUDE.md` + `README.md`, lists `divinecore-v2/`, runs `git log --oneline -20`, and reads `.claude/session.md` if present. Ends with a briefing on active modules, v2 stack state, and recent commit activity. Use this at the top of any non-trivial session. |
| `/resume` | Lightweight re-entry. Reads `CLAUDE.md` (and `.claude/session.md` if present) and gives a one-paragraph briefing: what was done last session, current state, single next action. |
| `/save-context` | Writes a ≤300-word session summary to `.claude/session.md` covering what changed, current state, decisions made, and the next step to resume from. Note: per commit `13faee3` we now lean on `git log` for progress tracking, so this is optional — use it only when the in-flight state genuinely won't be obvious from commit history. |

When adding new commands, keep them small and composable. One command, one job — same rule as agents.


## 15. TIERED CONTEXT CONVENTION (L0/L1/L2)

Inspired by ByteDance's OpenViking pattern. Every folder in this repo carries cheap, tiered context so an agent can scan the whole tree without paying full-file token costs.

| Tier | File | Size | When to load |
|------|------|------|--------------|
| **L0** | `.abstract.md` | ~1 line (max ~150 chars) | Always — reading every `.abstract.md` in the repo should fit in ~2k tokens. Answers "what is this folder for?" |
| **L1** | `.overview.md` | ~50–200 lines | When the L0 abstract suggests this folder is relevant. Covers structure, status, key files, conventions, what NOT to put here |
| **L2** | actual files | full content | Only when actively working in the folder |

### Rules

- **Every folder gets `.abstract.md`.** No exceptions, except:
  - Anything gitignored or tooling-internal (`.git/`, `__pycache__/`, `node_modules/`, `.venv/`).
  - `.claude/commands/` — Claude Code registers every `.md` file in that folder as a slash command, so `.abstract.md` would become a phantom `/.abstract` command. The folder itself is small enough to scan directly.
- **L1 `.overview.md` is selective.** Only for folders with real content, strategic importance, or non-obvious structure. Empty leaf scaffolds (`branding-os/agents/` while it's just a `.gitkeep`) get the abstract only — an overview would be noise.
- **Promote to L1 when the folder has 3+ files OR when the structure isn't self-explanatory.**
- **Update on change.** When you add/remove/rename meaningful content in a folder, update its `.abstract.md` and `.overview.md` in the same commit. Stale L0/L1 is worse than missing L0/L1.
- **Don't duplicate CLAUDE.md.** L0/L1 should describe local file structure, not repeat company-wide architecture. Architecture lives here in CLAUDE.md.

### AGENT BEHAVIOUR — MUST FOLLOW

These are not suggestions. Any agent (Claude Code, subagent, future tooling) working in this repo MUST follow them.

**On WRITE — when creating or modifying folder structure:**

1. **Creating a new folder?** In the same operation, create its `.abstract.md` (one line, max ~150 chars, "what is this folder for"). Do not commit a folder without its abstract — that breaks the L0 scan invariant.
2. **Adding 3+ real files to a folder, or making its structure non-obvious?** Add a `.overview.md` (50–200 lines: status, key files, conventions, what NOT to put here).
3. **Renaming or repurposing a folder?** Update its `.abstract.md` and any `.overview.md` in the same commit. Stale L0/L1 is worse than missing.
4. **Deleting a folder?** The `.abstract.md` and `.overview.md` go with it — never leave orphaned dotfiles.
5. **Skip only**: gitignored / tooling-internal folders (`.git/`, `__pycache__/`, `node_modules/`, `.venv/`) and `.claude/commands/` (would register as a slash command).

**On READ — when searching, exploring, or answering questions about the repo:**

1. **Start with `.abstract.md` files.** Glob `**/.abstract.md` and read them all. This costs ~2k tokens and gives you a complete repo map. Do this BEFORE any broad grep, file read, or directory listing.
2. **Drill into `.overview.md`** for any folder the abstracts flagged as relevant. Do not jump straight to L2 file contents.
3. **Open actual files (L2) only** in the folders the overviews confirmed are relevant.
4. **For known-path lookups** (you already know the file you need), skip L0/L1 and read the file directly — the tiered scan is for *open-ended* search, not targeted reads.

This keeps `/prime`-style context loads cheap and lets subagents do narrow lookups without ingesting the whole repo. Violating the L0-first rule on open-ended search wastes tokens — treat it as a bug.
