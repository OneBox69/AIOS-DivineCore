# Prime

Load full DivineCore context for this session. Do this in parallel where possible:

1. Read `CLAUDE.md` (architecture, modules, tech stack, conventions)
2. Read `README.md` (public-facing summary)
3. List `divinecore-v2/` to see the new FastAPI+Celery+Redis scaffold; read its README if present
4. Run `git log --oneline -20` to see recent activity
5. Read `.claude/session.md` if it exists (last session's handoff)

Then give a briefing covering:
- The five modules and which are active vs. planning
- Current state of the v2 stack (divinecore-v2/)
- What changed in the last ~20 commits
- Any open thread from the last session (if session.md exists)

End with: "Primed. What are we building?"
