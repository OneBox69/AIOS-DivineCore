# Prime

Load full DivineCore context for this session. Do this in parallel where possible:

1. Read `CLAUDE.md` (architecture, modules, tech stack, conventions — including §15 tiered context rules)
2. Read `README.md` (public-facing summary)
3. Read the root `.overview.md` (repo-wide map and entry-point pointers)
4. Glob `**/.abstract.md` and read every match — this is the L0 repo scan and should fit in ~2k tokens
5. Run `git log --oneline -20` to see recent activity
6. Read `.claude/session.md` if it exists (last session's handoff)

Then give a briefing covering:
- The five modules and which are active vs. planning (cross-reference what the abstracts say vs. CLAUDE.md §6)
- Current state of the v2 stack (`divinecore-v2/`)
- What changed in the last ~20 commits
- Any open thread from the last session (if `session.md` exists)
- Anything in the abstracts that looks stale relative to the git log (drift between L0 and reality)

End with: "Primed. What are we building?"
