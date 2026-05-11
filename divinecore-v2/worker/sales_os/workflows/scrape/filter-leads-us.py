"""
Post-Scrape Filter (US pipeline) — removes noise that Apollo's exclude filters don't catch.

Reads one or more scrape JSON files, dedupes by email/company_domain,
applies deterministic blacklist/whitelist rules against company_name, description,
and Apollo keywords field, writes cleaned JSON.

Three-layer filter architecture:
  1. NAME_BLACKLIST     — checked against company name only
  2. DESC_BLACKLIST     — checked against company description (specific phrases only)
  3. KEYWORDS_BLACKLIST — checked against Apollo keywords field (structured tags, high signal)
  4. NAME_WHITELIST     — name must contain an ICP signal (US ICPs: name only; others: name+desc)
  5. KEYWORDS whitelist — Apollo keywords field checked as fallback for generic-named companies

Usage:
  python execution/scrape/filter-leads-us.py <icp> <input1.json> [input2.json ...] --out <output.json>
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Substring matches against company_name (case-insensitive). If any matches → disqualify.
NAME_BLACKLIST = {
    "aesthetic-clinic-us": [
        # Home services — slip through via "aesthetic" in description
        "landscaping", "landscape", "lawn care", "lawn service", "lawn mowing",
        "cleaning service", "cleaning company", "janitorial", "maid service",
        "garage door", "garage floor", "flooring", "roofing", "solar panel",
        "solar energy", "pest control", "home services", "window cleaning",
        "deck builder", "gutter", "painting company",
        # Pet / non-medical services
        "pet spa", "pet salon", "dog grooming", "cat grooming", "grooming salon",
        "smoochie pooch", "spoiled paw",
        # Hair / nail salons
        "hair salon", "nail salon", "barbershop", "barber shop", "acqua aveda",
        # Franchise home services + skin franchise
        "bath tune-up", "n-hance wood", "granite garage", "grout doctor",
        "door renew", "garage guys", "array skin therapy",
        # Chains
        "ideal image", "laseraway", "sono bello", "milan laser",
        "massage envy", "hand & stone", "restore hyper wellness",
        "european wax center", "vio med spa", "sona medspa", "sona dermatology",
        "skin laundry", "skinspirit", "medspa810", "airsculpt",
        "national laser institute", "advanced medaesthetic", "alpha aesthetics partners",
        "inspire aesthetics", "olympus cosmetic", "princeton medspa",
        "empower aesthetics", "schweiger dermatology", "pinnacle dermatology",
        "us dermatology partners", "forefront dermatology",
        # B2B vendors
        "medical device", "medical supply", "equipment supplier", "pharmaceutical",
        "distributor", "wholesale", "allergan", "galderma", "merz aesthetics",
        "lumenis", "cutera", "syneron",
        # Training / education
        "training academy", "laser school", "aesthetics school", "certificate program",
        # Adjacent healthcare
        "dental", "dentist", "orthodont", "veterinary", "chiropractic",
        # Non-medical / portals
        "architecture", "interior design", "directory", "marketplace", "portal",
        "staffing", "recruitment",
    ],
    "real-estate-broker-us": [
        # Franchise brands
        "keller williams", "re/max", "remax", "coldwell banker", "century 21",
        "sotheby's", "berkshire hathaway homeservices", "bhhs", "weichert",
        "exp realty", "jpar", "compass", "redfin", "fathom realty", "better homes and gardens",
        "engel & volkers", "howard hanna", "long & foster", "nexthome", "homesmart",
        "realty one group", "united real estate", "anywhere real estate",
        "homeservices of america", "christie's international realty",
        # Property management / finance / portals
        "property management", "asset management", "reit", "investment trust",
        "mortgage", "title company", "escrow", "zillow", "realtor.com", "trulia",
        "opendoor", "offerpad", "proptech", "mls technology",
        "real estate software", "real estate crm",
        # Finance / lending / exchange intermediaries (not brokerage)
        "financial services", "1031 exchange", "qualified intermediary",
        "exchange company", "hard money", "private lending", "lending company",
        # Adjacent noise
        "home builder", "developer", "home inspection", "appraisal",
        "home warranty", "real estate training", "real estate coaching",
        "real estate marketing", "staffing", "recruitment",
        # Manufactured / mobile homes (not traditional brokerage)
        "manufactured homes", "mobile homes", "modular homes",
    ],
    "car-dealership-us": [
        # Large groups
        "autonation", "penske automotive", "lithia motors", "group 1 automotive",
        "sonic automotive", "asbury automotive", "hendrick automotive",
        "morgan auto group", "napleton automotive", "ken garff", "carmax",
        "carvana", "drivetime", "vroom", "echopark", "driveway", "america's car-mart",
        "manheim", "adesa", "copart",
        "matt bowers", "bud clary", "elway",
        # B2B consultants / non-dealers
        "consultant",
        # Golf cart / wrong vehicle type
        "golf",
        # Portals / marketplaces
        "autotrader", "cars.com", "cargurus", "truecar", "edmunds",
        # Rental / fleet
        "car rental", "rental car", "fleet management", "enterprise rent", "hertz",
        "avis", "turo",
        # Repair / parts / other
        "body shop", "collision center", "auto parts", "auto repair", "car wash",
        "auto auction", "auto transport", "insurance company", "finance company",
        "motorcycle dealer", "rv dealer", "boat dealer",
        # Automotive-adjacent but not dealers
        "career", "staffing", "training", "software", "technology",
        "trailer", "powersports", "equipment", "engineering",
    ],
}

# Substring matches against company_description (case-insensitive).
# Use specific phrases only — generic terms create false positives in free text.
DESC_BLACKLIST = {
    "car-dealership-us": [
        # Body shops
        "collision repair facility", "collision repair shop", "collision repair center",
        # Quick lube / oil change shops
        "oil change shop", "quick lube",
        # Metal manufacturers
        "metal stampings", "metal blanking",
        # Tooling shops
        "tool and die", "tool & die",
        # Industrial distributors / B2B vendors
        "industrial distributor", "industrial supplier", "mro supplier",
        # Vehicle manufacturer (not a dealer)
        "automaker", "vehicle manufacturer",
        # Van conversion shops
        "camper van conversion",
    ],
}

# Substring matches against Apollo keywords field (case-insensitive).
# Apollo's structured tags are highly reliable — much more so than free-text description.
KEYWORDS_BLACKLIST = {
    "car-dealership-us": [
        # Metal manufacturers
        "metal stamping", "metal blanking", "metal sheets",
        # Tooling / die shops
        "die repair", "die tryout", "die spotting",
        # Body shops
        "collision repair",
        # Machining / production manufacturing
        "production machining",
        # Auto accessory manufacturers
        "car mats", "floor liners",
        # Industrial MRO / distributors
        "bearings", "hydraulic & pneumatic components",
        "oil handling", "fluid handling",
        # B2B dealer equipment vendors
        "repair facility equipment", "automotive service equipment",
        # Van conversion / wrong vehicle type
        "camper van", "van builds",
        # ATV / powersports manufacturer
        "atv", "amphibious vehicles",
        # B2B dealership training / software vendors
        "dealership phone training", "dealership events", "automotive staffed events",
        # B2B dealer tech (DMS = Dealer Management System integrations)
        "dms polling",
        # B2B dealer photography / merchandising vendors
        "car photography", "lot merchandiser",
        # Golf carts
        "golf cart",
    ],
}

# Whitelist: at least one of these substrings MUST appear in company_name.
# For US ICPs we check name only (not description) to avoid noise like "aesthetic landscaping".
# Apollo keywords field is used as a fallback for generic-named companies.
NAME_WHITELIST = {
    "aesthetic-clinic-us": [
        "aesthetic", "aesthetics", "med spa", "medspa", "medical spa",
        "cosmetic", "plastic surgery", "skin clinic", "skin studio",
        "laser clinic", "laser center", "skin & laser", "rejuvenation",
        "botox", "filler", "injectable", "facial bar", "beauty bar",
        "dermatology", "dermatologist",
        "skin care", "skincare",
        "skin", "laser",
    ],
    "real-estate-broker-us": [
        "realty", "brokerage", "real estate", "properties", "realtor", "homes",
        "property group", "property co", "estates",
    ],
    "car-dealership-us": [
        # Generic dealership terms
        "motors", "automotive", "auto sales", "auto center", "auto group",
        "auto mart", "auto gallery", "car sales", "car dealer", "dealership",
        "pre-owned", "used cars", "used vehicles", "auto", "motor", "dealers",
        # Car brand names — dealerships named after their franchise brand
        "toyota", "honda", "ford", "chevrolet", "chevy", "dodge", "chrysler",
        "jeep", "ram", "gmc", "buick", "cadillac", "lincoln",
        "bmw", "mercedes", "audi", "volkswagen", "porsche", "volvo",
        "nissan", "hyundai", "kia", "subaru", "mazda", "mitsubishi",
        "lexus", "acura", "infiniti", "genesis",
        "jaguar", "land rover", "maserati", "alfa romeo",
    ],
}


def load_leads(paths: list[Path]) -> list[dict]:
    seen = set()
    leads = []
    for p in paths:
        items = json.loads(p.read_text(encoding="utf-8"))
        for l in items:
            # Dedup key: prefer email, fallback to domain+name
            key = (l.get("email") or "").lower()
            if not key:
                key = f"{(l.get('company_domain') or '').lower()}|{(l.get('company_name') or '').lower()}"
            if key in seen:
                continue
            seen.add(key)
            leads.append(l)
    return leads


def qualify(lead: dict, icp: str) -> tuple[bool, str]:
    name = (lead.get("company_name") or "").lower()
    desc = (lead.get("company_description") or "").lower()
    keywords = (lead.get("keywords") or "").lower()  # Apollo's own company tags — most reliable

    # Name blacklist — checked against company name only
    for term in NAME_BLACKLIST.get(icp, []):
        if term in name:
            return False, f"blacklist:{term}"

    # Description blacklist — specific phrases safe to match in free text
    for term in DESC_BLACKLIST.get(icp, []):
        if term in desc:
            return False, f"desc_blacklist:{term}"

    # Keywords blacklist — Apollo's structured tags, high signal
    for term in KEYWORDS_BLACKLIST.get(icp, []):
        if term in keywords:
            return False, f"keywords_blacklist:{term}"

    # Whitelist — two-layer check:
    # Layer 1: company name only (prevents "aesthetic landscaping" type noise)
    # Layer 2: Apollo keywords field (catches generic-named companies like "Elite Health Center"
    #          that have keyword tags like "aesthetic medicine, body contouring")
    whitelist = NAME_WHITELIST.get(icp, [])
    passes_name = any(term in name for term in whitelist)
    passes_keywords = any(term in keywords for term in whitelist) if keywords else False

    if not (passes_name or passes_keywords):
        return False, "whitelist:no_icp_signal"

    return True, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("icp")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    paths = [ROOT / p if not Path(p).is_absolute() else Path(p) for p in args.inputs]
    leads = load_leads(paths)

    kept, dropped = [], []
    for l in leads:
        ok, reason = qualify(l, args.icp)
        (kept if ok else dropped).append((l, reason))

    out_path = ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out_path.write_text(
        json.dumps([l for l, _ in kept], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Input total:   {len(leads)}")
    print(f"Kept:          {len(kept)}")
    print(f"Dropped:       {len(dropped)}")
    print()
    print("=== KEPT ===")
    for l, _ in kept:
        print(f"  {l.get('company_name'):<50} {l.get('country'):<15} {l.get('job_title')}")
    print()
    print("=== DROPPED ===")
    for l, r in dropped:
        print(f"  [{r}] {l.get('company_name'):<45} — {l.get('job_title')}")
    print()
    print(f"Match rate:    {len(kept)/len(leads)*100:.0f}%")
    print(f"Written to:    {out_path}")


if __name__ == "__main__":
    main()
