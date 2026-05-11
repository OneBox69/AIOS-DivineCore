# New Client Setup Guide
## From zero to a live lead pipeline in 5 steps

---

### What you're setting up

A fully automated monthly pipeline that:
1. Scrapes leads from Apollo via Apify
2. Filters and qualifies them against your ICP rules
3. Exports them to a Google Sheet
4. Generates personalised cold emails per lead
5. Runs follow-up sequences automatically via n8n

No manual work after setup.

---

### Prerequisites

Before you start, make sure you have:

- [ ] Google Cloud project with Sheets API enabled → `credentials.json` + `token.json`
- [ ] Apify account with Apollo scraper access
- [ ] n8n instance (cloud or self-hosted)
- [ ] `.env` file filled in (copy `.env.example`, add all keys)

---

## Step 1 — Create the client folder

```
clients/
└── your-client-name/
    ├── icps/
    │   └── your-icp-name/
    │       ├── scrape.yaml      ← copy from framework/scrape-template.yaml
    │       └── qualify.yaml     ← copy from framework/qualify-template.yaml
    └── templates/
        └── your-icp-email.yaml ← copy from framework/email-template.yaml
```

Fill in every `<FILL_IN>` placeholder in all three files.

---

## Step 2 — Fill in client-config.yaml

Copy `framework/client-config.yaml` to `clients/your-client-name/config.yaml`.

Fill in:
- `client_name`, `region`, `language`
- `sender_name`, `sender_company` (goes in email sign-off)
- For each ICP: `sheet_id`, paths to your scrape/qualify/email files
- The 4 `pain_questions` — rewrite these in your product's language

---

## Step 3 — Create the Google Sheet

```bash
python execution/export/create-sheet-us.py --client your-client-name --icp your-icp-name
# or for DACH:
python execution/export/create-sheet.py --client your-client-name --icp your-icp-name
```

This creates the sheet with the correct column schema. Copy the Sheet ID from the URL into your `client-config.yaml`.

---

## Step 4 — Run a test scrape (10 leads)

```bash
python execution/scrape/apify-scrape.py \
  --client your-client-name \
  --icp your-icp-name \
  --limit 10
```

Review the raw JSON output. Check:
- Are the companies actually your ICP?
- Are the job titles decision-makers?
- Any obvious noise to add to `scrape.yaml` exclusions?

If quality looks good, run the full scrape (50 leads).

---

## Step 5 — Filter, export, and generate copy

```bash
# Filter raw leads
python execution/scrape/filter-leads-us.py \
  --client your-client-name \
  --icp your-icp-name

# Export to Google Sheet
python execution/export/sheets-export-us.py \
  --client your-client-name \
  --icp your-icp-name

# Research leads (Phase 2a/2b) — assign signal type + phrase to each lead
# Currently manual or semi-automated (see research workflow)

# Generate copy once signals are in columns U + V
python scripts/generate-copy-us.py \
  --icp your-icp-name \
  --rows 2-50
```

---

## Step 6 — Import n8n workflows

Import these 4 workflow JSONs into your n8n instance:

| File | What it does |
|------|-------------|
| `n8n/workflows/positive-reply-research-v1.json` | Classifies inbound replies, notifies via Slack |
| `n8n/workflows/follow-up-pings-v1.json` | 5-stage auto follow-up (day 3/7/14/25/40) |
| `n8n/workflows/stage-auto-promote-v1.json` | Promotes lead stage when outbound is sent |
| `n8n/workflows/stalled-lead-reminder-v1.json` | Daily digest for exhausted leads |

After importing:
1. Update all credential references (Gmail, GHL, Instantly, Sheets, Slack)
2. Update any hardcoded Sheet IDs to your client's Sheet IDs
3. Read `n8n/conventions.md` before activating
4. Test each workflow with the sample payloads in `test-events/` before going live

---

## Folder structure after setup

```
clients/
└── your-client-name/
    ├── config.yaml
    ├── icps/
    │   └── your-icp-name/
    │       ├── scrape.yaml
    │       └── qualify.yaml
    └── templates/
        └── your-icp-email.yaml

data/
└── your-icp-name-YYYY-MM-DD.json           ← raw scrape output
└── your-icp-name-filtered-YYYY-MM-DD.json  ← post-filter output
```

---

## Monthly run checklist

- [ ] Trigger scrape (or let n8n cron fire automatically)
- [ ] Review filter output — any new noise to exclude?
- [ ] Run Phase 2a/2b research (assign signals to leads)
- [ ] Run generate-copy
- [ ] Review a sample of 5 emails before activating sequences
- [ ] Activate Instantly sequence with Sheet leads
- [ ] Monitor Slack for reply notifications

---

## Key rules (do not skip)

1. **Never send automated emails without client approval** — show copy first
2. **No hardcoded credentials** — everything via `.env` or n8n credential dropdowns
3. **Nothing goes live without testing** — run against 5 leads manually before full batch
4. **Read `n8n/conventions.md`** before touching any workflow
