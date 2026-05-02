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
└── shared/                    ← Shared utilities, base classes, common tools
    ├── utils/
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
