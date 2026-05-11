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
- #deploys — CI/CD status notifications from divinecore-v2 GitHub Actions (webhook configured in repo secrets as `DISCORD_WEBHOOK_URL`)


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
| Sales OS | Alex Hormozi — $100M Offers + $100M Leads books | Supabase (structured frameworks) |

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
- **Supabase (Core Knowledge Base):** Kallaway's lessons. Fields: Title, Category, Core Lesson, Full Explanation, Content Attributes, Content Types, Source URL, Notes. 61+ entries. Exact retrieval by category filter.
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

| Agent | Role |
|-------|------|
| Scout | Sales outreach agent — initiates and manages outbound contact across platforms |

Discord bot: Scout (APP)


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

DivineSide is run by **3 co-founders**. Detailed ownership and KPIs are being formalized in the May 2026 alignment meeting — this section will be updated post-meeting to reflect locked decisions.

| Name | Role | Notes |
|------|------|-------|
| Mayank Rawat | Co-founder · CEO, Engineering, Video Content | Owns product vision, system architecture, founder-led sales, all video content. Discord: mayank082527 |
| Shubham | Co-founder · Research & Ops | Owns Kallaway/Hormozi knowledge bases, pre-call audits, operational support |
| Pang (彭毅和) | Co-founder · Developer + Marketing | CS at Wuhan University, China. Owns pilot delivery, outbound engine, divinecore-v2 stack |


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

**External services**
- n8n: https://n8n.srv1445995.hstgr.cloud
- VPS: srv1445995.hstgr.cloud | IP: 187.124.96.99
- Airtable base: DivineCore
- Primary email (old): mayankrawat000072@gmail.com

**VPS SSH access** (`root@srv1445995.hstgr.cloud`)
- Pang (`yhpang@oneboxagency.com`) — authorized 2026-05-03. ed25519 key, no passphrase, generated on his Windows laptop at `C:\Users\user\.ssh\id_ed25519`. Personal access; CI auto-deploy will use a separate key when wired up.
- To grant or revoke a teammate's SSH access: edit `/root/.ssh/authorized_keys` on the VPS (one public key per line, comment field identifies the person).

**GitHub repository — `OneBox69/AIOS-DivineCore`** (Pang's fork, primary working repo)
- Upstream `DivineSide/AIOS-DivineCore` is currently stale; all active work happens on the fork.
- GitHub Actions secrets:
  - `GITHUB_TOKEN` — auto-provisioned, used to push images to GHCR.
  - `DISCORD_WEBHOOK_URL` — webhook for `#deploys` channel. Configured 2026-05-03.

**GitHub Container Registry (`ghcr.io/onebox69/aios-divinecore/{api,worker}`)**
- Images are **private**. Pulling requires auth.
- A classic PAT with `read:packages` scope only is cached on the VPS at `/root/.docker/config.json` (set up 2026-05-03 via `docker login ghcr.io -u onebox69 --password-stdin`). Rotate on PAT expiration.
- Anyone else pulling these images on a new machine needs to either be invited as a collaborator or generate their own `read:packages` PAT.


## 11. REPOSITORY STRUCTURE CONVENTIONS

```
DivineSide/
├── CLAUDE.md                  ← This file. Always keep updated.
├── README.md                  ← Public-facing repo overview
├── .env.example               ← Environment variable template (no real values)
├── branding_os/               ← Module 1: Creative Intelligence
│   ├── agents/                ← Agent definitions and system prompts
│   ├── knowledge-base/        ← KB management scripts
│   ├── workflows/             ← n8n workflow exports (JSON)
│   └── README.md
├── sales_os/                  ← Module 2: Revenue System
│   ├── agents/
│   ├── workflows/
│   ├── integrations/          ← Domain integrations (Upwork live)
│   │   └── upwork/            ← Celery tasks (proposal generation + sheet finalize)
│   └── web/                   ← FastAPI routers + Jinja templates mounted by divinecore-v2/api
│       └── upwork_routes.py + templates/
├── ops_os/                    ← Module 3: Execution System
│   ├── agents/
│   ├── workflows/
│   └── integrations/          ← Domain integrations (Fathom live)
│       └── fathom/            ← Celery poller + processor + tasks_writer
├── pulse/                     ← Module 4: Alert + Awareness
│   ├── agents/
│   ├── workflows/
│   └── README.md
├── networking_os/             ← Module 5: Networking & Recruitment
│   ├── agents/
│   ├── bots/
│   ├── workflows/
│   └── README.md
├── divinecore-v2/             ← Code-first runtime (FastAPI + Celery + Redis + compose)
│   ├── api/                   ← Generic FastAPI app; mounts routers from <module>/web/
│   └── worker/                ← Celery wiring + scheduled jobs; loads tasks from <module>/integrations/
├── infrastructure/            ← VPS, middleware, Discord bot, nginx configs
│   ├── discord-middleware/
│   └── README.md
└── shared/                    ← Shared resources used across modules
    ├── context/               ← Cross-module identity context (business-info, mayank, pang, voice, strategy, audience, linkedin-playbook). Every writing agent loads from here.
    ├── utils/                 ← Shared utilities, base classes, common tools
    └── README.md
```

**Folder naming**: module folders use Python-import-safe underscores (`sales_os/`, `branding_os/`, `ops_os/`, `networking_os/`, `pulse/`) so the divinecore-v2 runtime can import code from them as packages. Hyphens are reserved for non-Python directories (`divinecore-v2/`, `knowledge-base/`).

**Code vs n8n split**: each module folder mixes Python code (`integrations/`, `web/`, `agents/`), n8n workflow JSONs (`workflows/`), and KB sync scripts (`knowledge-base/`). The runtime that *executes* the Python lives in `divinecore-v2/`; the modules host their own logic and get imported.


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

Parallel track to the n8n-orchestrated stack. `divinecore-v2/` is the **runtime only** — FastAPI app, Celery worker, Beat scheduler, Redis broker, Docker compose. Domain code (Upwork, Fathom, future module integrations) lives in the module folders (`sales_os/`, `ops_os/`, etc.) and is imported by the runtime at build time. Both Dockerfiles set context = repo root and selectively `COPY` the module folders they need.

### Foundation (commit `3c03553`)

Stack: **FastAPI API + Celery worker + Celery Beat scheduler + Redis broker**, all in Docker Compose.

```
divinecore-v2/
├── api/                       ← FastAPI service (runtime only)
│   ├── main.py                ← Inline / + /tasks routes; imports + mounts routers from <module>/web/
│   ├── settings.py            ← Pydantic Settings (REDIS_URL)
│   ├── requirements.txt
│   └── Dockerfile             ← context = repo root; copies api/ + sales_os/
├── worker/                    ← Celery worker + beat (shares same image, runtime only)
│   ├── celery_app.py          ← Celery config + beat_schedule + include=[...] paths into modules
│   ├── tasks.py               ← echo, heartbeat (generic infra tasks)
│   ├── settings.py            ← Pydantic Settings (Supabase, OpenRouter, Fathom, Google OAuth, Redis)
│   ├── team.py                ← TEAM_MEMBERS dict + email/name lookup
│   ├── requirements.txt
│   └── Dockerfile             ← context = repo root; copies worker/ + sales_os/ + ops_os/
├── docker-compose.yml         ← local dev — context: .., volume mounts of api/, worker/, sales_os/, ops_os/, hot-reload
└── docker-compose.prod.yml    ← VPS deploy (image: from GHCR, no volume mounts, restart: unless-stopped, API behind Traefik basicauth)
```

Domain code mounted into the containers (lives outside `divinecore-v2/`):
- `sales_os/integrations/upwork/` — Upwork pipeline (Celery tasks)
- `sales_os/web/upwork_routes.py` + templates — `/upwork` UI mounted into FastAPI
- `ops_os/integrations/fathom/` — Fathom poller + processor (Celery tasks)

A repo-root `.dockerignore` trims build context size since context is now the whole repo.

Services in compose:
- `redis` — `redis:7-alpine`, exposes 6379
- `api` — FastAPI on `:8000`, talks to Celery via `REDIS_URL`
- `worker` — Celery worker, processes tasks from Redis
- `beat` — Celery Beat, runs scheduled tasks (currently `tasks.heartbeat` every 30s)

Endpoints today:
- `GET /` — health
- `POST /tasks/echo` — submit a task, returns `task_id`
- `GET /tasks/{task_id}` — poll status + result
- `GET /upwork` — Upwork proposal generator form (paste a job description). **Public**: https://upwork.srv1445995.hstgr.cloud/upwork (basic auth gated)
- `POST /upwork` — runs the Upwork pipeline (2 OpenRouter LLM calls + Google Docs/Drive/Sheets), blocks on result, renders application body + proposal Doc URL + a finalize form for connects/Loom
- `POST /upwork/finalize` — patches base+boosted connects ("15 + 5") and Loom URL into the existing tracking-sheet row
- `GET /upwork-jobs` — daily-scrape job queue (tabs: New / Skipped / Applied), sorted by Upwork posted_at desc. Basicauth-gated.
- `GET /upwork-jobs/{job_id}` — single-job detail with description + client stats + [Generate proposal] / [Skip] / [Unmark applied] buttons
- `POST /upwork-jobs/{id}/{skip,unskip,unmark-applied}` — flip review status
- `POST /upwork-jobs/{id}/generate` — runs the existing `tasks.upwork_generate_proposal` pipeline with the stored description, marks `applied` on success, renders the standard upwork result page

Run locally: `cd divinecore-v2 && docker compose up --build`. Public access details below in *Phase 2 → Public endpoints*.

### Integrations

- **Fathom** — beat polls Fathom's REST API every 10 min, writes new meetings to Supabase's `meetings` table, and creates Pulse task rows for action items assigned to opted-in team members. No public ingress required — fully outbound. **Lives in `ops_os/integrations/fathom/`** (Celery tasks `tasks.poll_fathom_recordings` etc., loaded by `divinecore-v2/worker/celery_app.py` `include=[...]`). See [ops_os/integrations/fathom/.overview.md](ops_os/integrations/fathom/.overview.md).
- **Upwork** — user-initiated via `GET /upwork` form. Originally migrated from a 3-workflow n8n system; the per-job sales-script Doc + Mermaid diagram step was dropped (Pang uses one standardised sales script across all calls; the Loom carries the AIOS framing). Today's pipeline: 2 OpenRouter LLM calls (proposal fields, application copy) + Google Docs/Drive/Sheets to copy the proposal template, mail-merge, share, and append to a tracking sheet. **Lives in `sales_os/integrations/upwork/`** (Celery tasks) + `sales_os/web/upwork_routes.py` (FastAPI router). About-Me content lives in `sales_os/integrations/upwork/about_me.py` — Upwork-specific, intentionally stripped of "co-founder" / "agency" framing (some buyers are agency-averse); loosely derived from [shared/context/pang.md](shared/context/pang.md) but **not** an auto-mirror — edit directly when needed. Application body prompt enforces the AIOS framing (verbatim sentence: *"I don't build commoditized automations. I build AI Operating Systems — your business, running on AI."*) — this deliberately diverges from sales-playbook.md line 173 ("never lead with AIOS externally") because on Upwork specifically AIOS is the differentiator that justifies the price floor. Google auth via OAuth refresh token — one-time bootstrap with `docker compose run --rm worker python -m sales_os.integrations.upwork.oauth_bootstrap`. Env vars: `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`, plus optional `UPWORK_*` model/template-ID overrides. See [sales_os/integrations/upwork/.overview.md](sales_os/integrations/upwork/.overview.md).
- **Instantly** — cold-email outreach (current positioning: *UK ecom beauty 5–50 employees*). Webhook ingress at public `POST /instantly/webhook` validates a shared `X-Webhook-Secret` header and enqueues a Celery task that stores meaningful replies (skipping OOO/auto-replies) to Supabase `outreach_replies` and pings the `outreach-replies` thread inside `#sales-and-outreach` for any reply Instantly's AI labels positive (configurable set in `categories.py`). **No LLM classification on our side** — we trust Instantly's labels. **No per-email-send rows** — a daily 00:30 UTC Celery beat task (`tasks.poll_instantly_campaigns`) snapshots Instantly's campaign + step analytics into `outreach_daily_step_metrics` (one row per campaign × step × day). Operator owns `outreach_campaigns.positioning` (set manually in Supabase Studio after the first poll lands the row; the poller's upsert never overwrites it). Reporting dashboard lives at `GET /outreach` (basicauth) — campaign list + per-campaign drill-in with per-step / daily / lifetime metrics + recent replies feed. **Lives in `sales_os/integrations/instantly/`** (Celery tasks + Supabase + Discord) + `sales_os/web/instantly_routes.py` (webhook + dashboard). Traefik routes the public webhook via a separate router (`instantly-webhook` priority 100) that bypasses the basicauth middleware applied to the rest of `upwork.srv1445995.hstgr.cloud`. Env vars: `INSTANTLY_API_KEY`, `INSTANTLY_WEBHOOK_SECRET`, `DISCORD_OUTREACH_WEBHOOK_URL`, `DISCORD_OUTREACH_THREAD_ID`, plus optional `INSTANTLY_API_BASE_URL`. See [sales_os/integrations/instantly/.overview.md](sales_os/integrations/instantly/.overview.md).
- **Upwork jobs feed (Apify)** — daily Apify-driven scrape of a single saved-search URL into a manual review queue. Beat fires `tasks.poll_upwork_jobs` once a day at **21:40 UTC (= 05:40 MYT)**, which calls the `neatrat/upwork-job-scraper` Apify actor with `rawUrl=UPWORK_SEARCH_URL` and upserts each item into Supabase `upwork_jobs`. **No auto-drafting, no scoring, no Discord** — Pang reads through the queue at `GET /upwork-jobs` (basicauth), and only when he clicks **Generate proposal** does the existing `tasks.upwork_generate_proposal` pipeline run on the stored description (then the row gets marked `applied`). Operator-owned columns (`status`, `reviewed_at`, `applied_at`, `proposal_doc_url`) are excluded from the daily upsert via PostgREST's `?columns=` so re-fetched jobs keep their review state. Why Apify and not the official Upwork GraphQL API: the official API requires a partner application that takes weeks; Apify rotates *its own* cookies + proxies, so the ToS / detection risk lives on Apify's side rather than on Pang's account. Cost: ~$3-10/mo at one-run-per-day volume ($3.20/1000 jobs, min 10-job bill per run). **Lives in `sales_os/integrations/upwork_jobs/`** (apify_client + supabase_writer + processor) + `sales_os/web/upwork_jobs_routes.py` (queue UI). Env vars: `APIFY_API_TOKEN`, `UPWORK_SEARCH_URL`, plus optional `APIFY_UPWORK_ACTOR_ID`. See [sales_os/integrations/upwork_jobs/.overview.md](sales_os/integrations/upwork_jobs/.overview.md).

### CI/CD Workflow (commit `3573662`)

File: `.github/workflows/divinecore-v2-ci.yml`

Triggers: push/PR to `main` (path-filtered to `divinecore-v2/**`, `sales_os/**`, `ops_os/**`, and the workflow file itself) + `workflow_dispatch`.

**Build & push job** (matrix: `api`, `worker`):
- Runs both components in parallel via matrix strategy
- Build context is the repo root; `dockerfile:` matrix entry points at `divinecore-v2/{api,worker}/Dockerfile`
- Uses `docker/setup-buildx-action@v3` + `docker/build-push-action@v6`
- Pushes to `ghcr.io/onebox69/aios-divinecore/{api,worker}`
- Tags: `:latest` (main only), `:sha-<short>`, `:<branch>`
- GHA cache scoped per component (`cache-from/to` with `scope=${name}`) — fast incremental rebuilds
- PRs are build-only (no push to GHCR, no Discord ping) — gated on `github.event_name != 'pull_request'`

**Notify job:**
- Runs after `build-and-push` on push + workflow_dispatch (excludes PR builds — see PR #2)
- Uses `sarisia/actions-status-discord@v1`
- Posts status embed (success/failure) to `#deploys` via `DISCORD_WEBHOOK_URL` secret
- Embed includes branch + commit message

Required GitHub secrets:
- `GITHUB_TOKEN` — provided automatically, used for GHCR auth
- `DISCORD_WEBHOOK_URL` — webhook for `#deploys` channel (configured on `OneBox69/AIOS-DivineCore`, end-to-end verified 2026-05-03)

Permissions on the build job: `contents: read`, `packages: write` (needed to push to GHCR).

### Phase 2 — Deployed (manual deploy live, auto-deploy still pending)

The stack is **running on the Hostinger VPS** at `/root/divinecore-v2/` as of 2026-05-03. Deployed manually over SSH; CI does not yet auto-deploy on merge.

**What's running on the VPS:**
- `divinecore-v2-redis-1` — internal compose network only, no port exposure
- `divinecore-v2-api-1` — FastAPI on port 8000 (no host port binding); attached to `divinecore` bridge AND `n8n_default` external network so n8n's Traefik can route to it
- `divinecore-v2-worker-1` — Celery worker, connected to Redis
- `divinecore-v2-beat-1` — Celery Beat, scheduling `tasks.heartbeat` every 30s
- All four `restart: unless-stopped`, isolated from n8n's containers via dedicated `divinecore` bridge network (api additionally joins `n8n_default` for Traefik discovery)

**GHCR auth on VPS:** `docker login ghcr.io` configured with a GitHub PAT (`read:packages` scope only). Credentials cached in `/root/.docker/config.json` — required for pulling private images on each `docker compose pull`. Rotate the PAT on its expiration.

**Manual deploy procedure** (from local laptop):
```
ssh root@srv1445995.hstgr.cloud "cd /root/divinecore-v2 && docker compose pull && docker compose up -d"
```

**Smoke test verified:** `POST /tasks/echo` → task queued in Redis → worker processes → `GET /tasks/{id}` returns `SUCCESS` with uppercased result. Full async pipeline working end-to-end on VPS.

### Public endpoints

**`/upwork` is live publicly** at `https://upwork.srv1445995.hstgr.cloud/upwork` (deployed 2026-05-04). Routed through n8n's existing Traefik (the only reverse proxy on the VPS — `n8n-traefik-1`, ports 80/443).

Wiring:
- The api service in `docker-compose.prod.yml` carries `traefik.*` labels (Host rule, `websecure` entrypoint, `tls=true`, basicauth middleware). Traefik picks them up via Docker socket events.
- api is attached to the external `n8n_default` network (declared at compose bottom as `networks.traefik`) — that's how Traefik reaches the container.
- **Basic auth** via `traefik.http.middlewares.upwork-auth.basicauth.users` label. Bcrypt hash inline, dollar signs escaped as `$$` per compose syntax. Username/password live in your password manager — to rotate, generate a new hash with `docker run --rm httpd:2.4-alpine htpasswd -nbB <user> <pass>`, double the `$`, replace the label, push, redeploy.
- **TLS cert is Traefik's default self-signed.** Browser shows a one-time "Not secure" warning per device — click through, browser remembers the exception. Reason: Let's Encrypt rate-limited the `*.hstgr.cloud` apex (25k certs in 7d, shared across all Hostinger users on the domain), so `tls.certresolver=mytlschallenge` returned `429 rateLimited` and was removed. To upgrade to a real cert: migrate to a domain outside the rate-limited apex (~$1–12/yr for a `.xyz`/`.com`), or wait for LE quota to roll over, then re-add the certresolver label.

n8n's `web` (HTTP) entrypoint has a global `--entrypoints.web.http.redirections.entryPoint.to=websecure` set in Traefik's command line — all HTTP traffic gets 308'd to HTTPS automatically. This is shared with n8n; don't change it without auditing n8n impact.

**Still pending:**
- **Auto-deploy from CI.** Add a `deploy` job to `divinecore-v2-ci.yml` that SSHes into VPS after each successful `build-and-push` on main and runs the manual deploy command above. Needs a separate deploy SSH keypair + 3 GitHub secrets (`VPS_SSH_PRIVATE_KEY`, `VPS_HOST`, `VPS_USER`). Mayank's personal SSH key is already authorized on the VPS as of 2026-05-03; CI will use a different key.
- **Trusted TLS cert for upwork.* subdomain.** Currently default self-signed (browser warning). Upgrade path: switch to a domain outside `hstgr.cloud`, OR retry LE periodically.


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
- **L1 `.overview.md` is selective.** Only for folders with real content, strategic importance, or non-obvious structure. Empty leaf scaffolds (`branding_os/agents/` while it's just a `.gitkeep`) get the abstract only — an overview would be noise.
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
