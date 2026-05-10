"""
Apify Scrape — code_crafter/leads-finder (Apollo wrapper).

Usage:
  python execution/scrape/apify-scrape.py <icp-name> [--count 50] [--wait]

Reads filters from clients/moic-ai/icps/<icp-name>/scrape.yaml.
Writes raw output to data/<icp-name>-YYYY-MM-DD.json.
"""

import argparse
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
TOKEN = os.environ["APIFY_API_TOKEN"]
ACTOR = "code_crafter~leads-finder"

# Apify size buckets — derived from employee_count min/max in scrape.yaml
SIZE_BUCKETS = [
    ("1-10", 1, 10),
    ("11-20", 11, 20),
    ("21-50", 21, 50),
    ("51-100", 51, 100),
    ("101-200", 101, 200),
    ("201-500", 201, 500),
    ("501-1000", 501, 1000),
    ("1001-2000", 1001, 2000),
    ("2001-5000", 2001, 5000),
    ("5001-10000", 5001, 10000),
    ("10001-20000", 10001, 20000),
    ("20001-50000", 20001, 50000),
]


def pick_sizes(min_emp: int, max_emp: int) -> list[str]:
    return [label for label, lo, hi in SIZE_BUCKETS if hi >= min_emp and lo <= max_emp]


def build_input(cfg: dict, count: int, file_name: str) -> dict:
    f = cfg["filters"]
    ec = f["employee_count"]

    # Flatten exclude_companies.chains into not_keywords
    chains = cfg.get("filters", {}).get("exclude_companies", {}).get("chains") or []
    chains = chains + (cfg.get("exclude_companies", {}).get("chains") or [])
    # scrape.yaml uses top-level or nested; handle both
    top_chains = cfg.get("exclude_companies", {}).get("chains") or []
    all_chains = list(set(chains + top_chains))

    not_keywords = list(f["company_keywords"].get("exclude_any", [])) + all_chains

    return {
        "fetch_count": count,
        "file_name": file_name,
        "contact_job_title": f["titles"]["include"],
        "contact_not_job_title": f["titles"]["exclude"],
        "seniority_level": cfg.get("seniority_level", ["founder", "owner", "c_suite"]),
        "contact_location": f["locations"],
        "company_industry": f["industries"]["include"],
        "size": pick_sizes(ec["min"], ec["max"]),
        "company_keywords": f["company_keywords"]["include_any"],
        "company_not_keywords": not_keywords,
        "email_status": ["validated"],
    }


def start_run(payload: dict) -> str:
    url = f"https://api.apify.com/v2/acts/{ACTOR}/runs?token={TOKEN}"
    r = requests.post(url, json=payload, timeout=60)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code}: {r.text[:500]}")
    r.raise_for_status()
    run = r.json()["data"]
    return run["id"], run["defaultDatasetId"]


def wait_for_run(run_id: str, poll: int = 10) -> str:
    url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={TOKEN}"
    while True:
        r = requests.get(url, timeout=30).json()["data"]
        status = r["status"]
        print(f"  [{r.get('stats',{}).get('runTimeSecs', '?')}s] status={status}")
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            return status
        time.sleep(poll)


def fetch_dataset(dataset_id: str) -> list[dict]:
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={TOKEN}&format=json&clean=true"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("icp")
    ap.add_argument("--client", default="moic-ai", help="Client folder (moic-ai, oac, etc.)")
    ap.add_argument("--count", type=int, default=50)
    ap.add_argument("--wait", action="store_true", help="Block until run finishes")
    ap.add_argument("--suffix", default="", help="Tag für Output-Datei (z.B. 'v2')")
    args = ap.parse_args()

    cfg_path = ROOT / "clients" / args.client / "icps" / args.icp / "scrape.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    today = date.today().isoformat()
    stem = f"{args.icp}-{args.suffix + '-' if args.suffix else ''}{today}"
    file_name = stem + "-apify"

    payload = build_input(cfg, args.count, file_name)
    print(f"ICP:        {args.icp}")
    print(f"Count:      {args.count}")
    print(f"Industries: {payload['company_industry']}")
    print(f"Sizes:      {payload['size']}")
    print(f"Keywords+:  {len(payload['company_keywords'])} items")
    print(f"Keywords-:  {len(payload['company_not_keywords'])} items")
    print()

    run_id, dataset_id = start_run(payload)
    print(f"Run started: {run_id}")
    print(f"Dataset:     {dataset_id}")
    print(f"Console:     https://console.apify.com/actors/runs/{run_id}")

    if not args.wait:
        print("\nUse --wait to block until finished, or rerun with --wait later.")
        return

    print("\nWaiting for run to finish...")
    status = wait_for_run(run_id)
    if status != "SUCCEEDED":
        print(f"Run {status}. Aborting.")
        sys.exit(1)

    items = fetch_dataset(dataset_id)
    out_path = ROOT / "data" / f"{stem}.json"
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(items)} leads written to {out_path}")


if __name__ == "__main__":
    main()
