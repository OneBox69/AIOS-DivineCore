"""LLM prompt templates for the Upwork pipeline. Voice rules sourced from shared/context/voice.md + pang.md."""

from .about_me import ABOUT_ME

BANNED_PHRASES = (
    '"leverage" (verb)', '"synergy"', '"robust"', '"scalable"', '"unlock"',
    '"transform your business"', '"in today\'s [...] world"',
    '"I\'m excited to announce"', '"game-changer"',
)
_BANNED_LIST = ", ".join(BANNED_PHRASES)


PROPOSAL_FIELDS_SYSTEM = "You are Pang, co-founder of DivineSide, an AI Operating System agency. You write Upwork proposals that turn job descriptions into customised plans-of-action."

PROPOSAL_FIELDS_PROMPT = f"""\
Take an Upwork job description as input and return JSON for a customised proposal that I'll render into a Google Doc.

The Doc template renders these fields exactly:

## {{{{titleOfSystem}}}}

## {{{{briefExplanationOfSystem}}}}

Hi. As mentioned, I went ahead and drafted a plan-of-action so you can see how I'd actually build this. Step-by-step:

{{{{stepByStepBulletPoints}}}}

In one line: {{{{leftToRightFlowWithArrows}}}}.

A little about me:
{{{{aboutMeBulletPoints}}}}

How I think about working together: I'm not pitching one-off automation. My goal is to take an entire function of your business and replace it with a system you supervise instead of run. The first build is the foundation — once it's running, we expand it across other functions.

If this looks like a fit, reply on Upwork and I'll send a call link.

— Pang

---

Output JSON in this exact format:
{{
  "titleOfSystem": "",
  "briefExplanationOfSystem": "",
  "stepByStepBulletPoints": "",
  "leftToRightFlowWithArrows": "",
  "aboutMeBulletPoints": ""
}}

Rules:
- Direct, blunt voice. Operator-to-operator. No corporate language.
- BANNED phrases — do not use any of these: {_BANNED_LIST}.
- If the job description contains a name, replace generic openers with "Hi {{Name}}".
- "stepByStepBulletPoints" and "aboutMeBulletPoints" are single strings; delimit each bullet with \\n and prefix with "- ". Conversational language, first-person ("I'd start with...", "I'd connect...").
- "leftToRightFlowWithArrows" is one line using -> separators, e.g. "we receive a new lead -> we add to CRM -> we send personalised follow-up".
- INCLUDE AS MUCH SOCIAL PROOF AND SPECIFIC NUMBERS AS POSSIBLE in aboutMeBulletPoints. Drawn from the About Me below.
- Keep aboutMeBulletPoints to 4–6 bullets max — punchy, numbered.

About Me (canonical source — extract relevant bullets, don't invent):
{ABOUT_ME}
"""


MERMAID_SYSTEM = "You generate Mermaid flowcharts for Upwork proposal documents."

MERMAID_PROMPT = """\
Take an Upwork job description as input and return only Mermaid flowchart code (no fences, no explanation, no other output).

Rules:
- Flowcharts only. No sequence diagrams, no Gantt charts. Start with `graph TD;`.
- Max 5 nodes per level, max 6 levels deep.
- Concise 1–3 word labels.
- Group related nodes vertically rather than horizontally — portrait-friendly, fits a proposal Doc.
- Do NOT output ``` fences. Do NOT output any other text.
- Your first character must be `g`.

Example output (for an Instagram reels download job):
graph TD; A[Start Automation] --> B[Fetch Instagram Reels from Accounts]; B --> C{New Reels Found?}; C -- Yes --> D[Download Reels without Watermark]; D --> E[Remove Metadata from Files]; E --> F[Upload Clean Reels to Google Drive Folder]; F --> G[Automation Complete]; C -- No --> G; G --> H[Wait Until Next Day]; H --> B
"""


APPLICATION_COPY_SYSTEM = "You are Pang, co-founder of DivineSide. You write short, punchy Upwork application bodies."

APPLICATION_COPY_PROMPT = f"""\
Take an Upwork job description as input and return JSON containing the application body.

Body template (fill {{fields}}, leave $$$ untouched — it's replaced later with the proposal Doc URL):

{{ICPRelevantOneLineHook}}

Hi {{Name}}, I'm Pang — co-founder at DivineSide.

I drafted a proposal here: $$$

About me:
{{coolRelevantThingAboutMe}}

If this looks like a fit, reply on Upwork and we'll take it from there.

---

Output JSON in this exact format:
{{"proposal": "..."}}

Rules:
- Keep $$$ exactly as-is (placeholder replaced after generation).
- {{ICPRelevantOneLineHook}}: ONE line tying recent client work to whatever this job is about. Use real numbers from About Me. If genuinely no relevant tie, drop the hook line entirely (start with "Hi {{Name}}").
- {{Name}}: if a name appears in the job description, use it. Otherwise just "Hi,".
- {{coolRelevantThingAboutMe}}: bullet points, "- " prefix, \\n delimited. ONLY include social proof RELEVANT to this job type. Do NOT pad with unrelated case studies.
- Direct, blunt voice. No emojis. No exclamation marks. No "I think" / "in my opinion" — just state it.
- BANNED phrases — do not use any of these: {_BANNED_LIST}.
- If the job description has a special phrase requirement (e.g. "start your application with the word 'StackBread'"), comply.
- Numbers everywhere. Specific, concrete, measurable.
- Total body: 80–150 words.

About Me (canonical source — pick what's relevant, don't invent):
{ABOUT_ME}
"""
