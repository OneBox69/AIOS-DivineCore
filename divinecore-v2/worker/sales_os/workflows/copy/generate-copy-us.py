"""
Lead Copy Generator — US ICPs only.

Reads leads from Google Sheet, uses Style column (U) + Phrase column (V) +
lead data (A-R) to generate copy. Writes copy to columns S-Z.

Usage:
    python scripts/generate-copy-us.py --icp aesthetic-clinic-us --rows 2,3,4
    python scripts/generate-copy-us.py --icp real-estate-broker-us --all-signaled
    python scripts/generate-copy-us.py --icp car-dealership-us --rows 2-9 --dry-run

Prerequisite: Columns U + V already filled (by Phase 2a + 2b).
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import quote

import yaml
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession, Request

ROOT = Path(__file__).resolve().parent.parent
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TEMPLATES_DIR = ROOT / "templates" / "us"
BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"

SHEET_IDS = {
    "aesthetic-clinic-us": "1Y-6-6Alg9USNuIvERx18k8cJ_cN1-2BxgqjAUn5p9ng",
    "real-estate-broker-us": "1wGd3qr2cJ4NllU5PlZ3SSvB5R-bxWbpct_lxsF6yNpk",
    "car-dealership-us": "17CDOLo_jnm5ffpYVkYEGF4xOZnZxxprKbCeesKXJeuE",
}

PAIN_QUESTION = {
    "pain_fwd_reactivation": "Quick question — how are you currently staying in touch with customers from 1-2 years ago?",
    "pain_fwd_reception": "Quick question — how do you handle inquiries that come in evenings or weekends?",
    "pain_fwd_speed": "Quick question — what happens to inquiries when no one's available to respond right away?",
    "pain_fwd_upsell": "Quick question — how are you currently approaching existing customers about additional services?",
}

MASTER_TAB = "All Leads"


def load_templates(icp: str) -> dict:
    path = TEMPLATES_DIR / f"{icp}-email.yaml"
    text = path.read_text(encoding="utf-8")
    templates = {}
    for doc in yaml.safe_load_all(text):
        if not doc:
            continue
        if "signal_type" in doc:
            templates[doc["signal_type"]] = doc
    return templates


def get_session() -> AuthorizedSession:
    creds = Credentials.from_authorized_user_file(ROOT / "token.json", SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        (ROOT / "token.json").write_text(creds.to_json())
    return AuthorizedSession(creds)


def sheets_get(session: AuthorizedSession, sid: str, range_: str) -> dict:
    url = f"{BASE_URL}/{sid}/values/{quote(range_, safe='')}"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def sheets_update(session: AuthorizedSession, sid: str, range_: str, values: list):
    url = f"{BASE_URL}/{sid}/values/{quote(range_, safe='')}?valueInputOption=RAW"
    r = session.put(url, json={"values": values}, timeout=30)
    r.raise_for_status()
    return r.json()


def find_scrape_tab(session: AuthorizedSession, sid: str) -> str | None:
    r = session.get(f"{BASE_URL}/{sid}", timeout=30)
    r.raise_for_status()
    meta = r.json()
    scrape_tabs = [
        s["properties"]["title"]
        for s in meta.get("sheets", [])
        if s["properties"]["title"].startswith("Scrape ")
    ]
    return sorted(scrape_tabs)[-1] if scrape_tabs else None


def parse_style(style_cell):
    s = style_cell.strip()
    for variant in [
        "pain_fwd_reactivation", "pain_fwd_reception", "pain_fwd_speed",
        "pain_fwd_upsell", "fallback",
    ]:
        if s.startswith(variant):
            path = "fallback" if "(fallback)" in s else "primary"
            return variant, path
    return None, None


def determine_salutation(first_name, last_name):
    """US norm: first name only."""
    fn = (first_name or "").strip()
    ln = (last_name or "").strip()
    return fn or ln


def build_opener_line(variant, path, phrase_or_observation):
    pain_q = PAIN_QUESTION[variant]
    if path == "primary":
        phrase = phrase_or_observation.strip('"').strip('„').strip('"').strip()
        return f'your site says "{phrase}" — {pain_q}'
    else:
        return f"just looked at your site — {phrase_or_observation}. {pain_q}"


def generate_copy(templates, variant, first_name, opener_line, company_name, founded_year):
    tmpl = templates.get(variant)
    if not tmpl:
        return None, None, None, None

    ft_subject = tmpl["first_touch"]["subject"]
    ft_body = tmpl["first_touch"]["body"]
    st_subject = tmpl["second_touch"]["subject"]
    st_body = tmpl["second_touch"]["body"]

    replacements = {
        "{{first_name}}": first_name,
        "{{opener_line}}": opener_line or "",
        "{{company_name}}": company_name or "",
        "{{founded_year}}": str(founded_year or ""),
    }
    for old, new in replacements.items():
        ft_subject = ft_subject.replace(old, new)
        ft_body = ft_body.replace(old, new)
        st_subject = st_subject.replace(old, new)
        st_body = st_body.replace(old, new)

    return ft_subject.strip(), ft_body.strip(), st_subject.strip(), st_body.strip()


def pflicht_check(first_touch):
    word_count = len(first_touch.split())
    body_no_sig = first_touch.replace("MOIC AI", "")
    has_ki = " AI " in body_no_sig
    checks = {
        "under_150_words": word_count < 150,
        "no_AI_mention": not has_ki,
    }
    return all(checks.values()), checks, word_count


def parse_rows_arg(rows_str):
    rows = []
    for part in rows_str.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            rows.extend(range(int(a), int(b) + 1))
        else:
            rows.append(int(part))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--icp", required=True, choices=list(SHEET_IDS.keys()))
    parser.add_argument("--rows", help="Row numbers, e.g. 2,3,4 or 2-9")
    parser.add_argument("--all-signaled", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sid = SHEET_IDS[args.icp]
    templates = load_templates(args.icp)
    print(f"ICP: {args.icp} | Sheet: {sid[:12]}... | Templates: {list(templates.keys())}")

    session = get_session()
    scrape_tab = find_scrape_tab(session, sid)
    print(f"Scrape tab: {scrape_tab}")

    if args.rows:
        target_rows = parse_rows_arg(args.rows)
    elif args.all_signaled:
        r = sheets_get(session, sid, f"'{MASTER_TAB}'!S2:S200")
        stages = r.get("values", [])
        target_rows = [i + 2 for i, s in enumerate(stages) if s and s[0] == "signaled"]
    else:
        print("Please specify --rows or --all-signaled.")
        sys.exit(1)

    print(f"Rows: {target_rows}\n")

    for row in target_rows:
        r = sheets_get(session, sid, f"'{MASTER_TAB}'!A{row}:V{row}")
        data = r.get("values", [[]])[0]
        while len(data) < 22:
            data.append("")

        first_name, last_name = data[0], data[1]
        company = data[8]
        founded_year = data[17]
        style_cell = data[20]
        phrase_or_obs = data[21]

        if not style_cell:
            print(f"  Row {row} | {company} | NO STYLE -> skip")
            continue

        variant, path = parse_style(style_cell)
        if not variant:
            print(f"  Row {row} | {company} | UNKNOWN STYLE: {style_cell} -> skip")
            continue

        first_name_clean = determine_salutation(first_name, last_name)

        opener_line = ""
        if variant.startswith("pain_fwd_"):
            opener_line = build_opener_line(variant, path, phrase_or_obs)

        ft_subj, ft_body, st_subj, st_body = generate_copy(
            templates, variant, first_name_clean, opener_line, company, founded_year
        )

        if not ft_body:
            print(f"  Row {row} | {company} | Template '{variant}' not found -> skip")
            continue

        ok, checks, wc = pflicht_check(ft_body)
        status = "PASS" if ok else "FAIL"
        print(f"  Row {row:3} | {company[:30]:30} | {variant} ({path}) | {wc}W | {status}")

        if not ok:
            for k, v in checks.items():
                if not v:
                    print(f"    FAIL: {k}")
            continue

        if args.dry_run:
            continue

        r_t = sheets_get(session, sid, f"'{MASTER_TAB}'!T{row}")
        research = r_t.get("values", [[""]])[0][0] if r_t.get("values") else ""

        values = [["copy_done", research, style_cell, phrase_or_obs, ft_subj, ft_body, st_subj, st_body]]

        for tab in [MASTER_TAB] + ([scrape_tab] if scrape_tab else []):
            try:
                sheets_update(session, sid, f"'{tab}'!S{row}:Z{row}", values)
            except Exception as e:
                print(f"    {tab}: ERROR {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
