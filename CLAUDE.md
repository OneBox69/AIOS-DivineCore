# DivineSide Client Discovery Agent

**Owner:** Mayank  
**Company:** DivineSide — an AI OS agency

## Purpose

Build a Client Discovery Agent that researches potential clients, scores their fit, and generates personalised outreach emails.

## Tech Stack

- Python 3.14
- OpenAI API (key stored in `.env` as `OPENAI_API_KEY`)
- `python-dotenv` for environment variables
- Virtual environment in `.venv/`

## Project Files

- `agent.py` — main entry point (skeleton only, logic not built yet)
- `.env` — contains `OPENAI_API_KEY` (excluded from git)
- `.gitignore` — excludes `.env` and `.venv`

## Agent Behaviour (Next Step)

Build the full agent logic inside `agent.py`:

1. Accept company name and website URL as input
2. Fetch and parse the website content
3. Analyse with OpenAI: what they do, pain points, DivineSide fit
4. Score client fit 0–100 with reasoning
5. Generate a personalised outreach email
6. Save the full report to a file

## Conventions

- Keep all logic in `agent.py` until the codebase grows enough to split
- Use `python-dotenv` — never hardcode keys
- Save reports as `reports/<company_name>_<date>.txt`
