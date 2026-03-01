"""
SHL Assessment Catalog Scraper - Fixed Version
Properly parses test_types, duration, remote_testing from SHL catalog.

QUICK FIX (no re-scraping):
  python src/scraper.py --fix-only data/shl_assessments.json

FULL SCRAPE:
  python src/scraper.py data/shl_assessments.json
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
VALID_TYPES = set("ABCKPS")


def split_test_types(raw):
    """
    "CPAB" or ["CPAB"] or "C" -> ["C","P","A","B"]
    Handles every format the scraper might produce.
    """
    if isinstance(raw, list):
        raw = "".join(str(x) for x in raw)
    return list(dict.fromkeys(c for c in str(raw).upper() if c in VALID_TYPES))


def get_page(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None


def parse_catalog_page(html):
    soup = BeautifulSoup(html, "html.parser")
    assessments = []
    seen_urls = set()

    for link in soup.select('a[href*="/product-catalog/view/"]'):
        href = link.get("href", "")
        if not href:
            continue
        url = urljoin(BASE_URL, href)
        if url in seen_urls:
            continue
        seen_urls.add(url)
        name = link.get_text(strip=True)
        if not name:
            continue

        row = link.find_parent("tr")
        test_types = []
        remote_testing = False
        adaptive = False

        if row:
            for cell in row.find_all("td"):
                cell_text = cell.get_text(strip=True)
                classes = " ".join(cell.get("class", []))

                # Test types: "CPAB" or "K" etc.
                if re.match(r'^[ABCKPS]{1,6}$', cell_text):
                    test_types = split_test_types(cell_text)

                # Remote / adaptive: check for -yes images
                for img in cell.find_all("img"):
                    src = img.get("src", "").lower()
                    alt = img.get("alt", "").lower()
                    is_yes = "-yes" in src or "check" in src or "yes" in alt
                    if is_yes:
                        if "remote" in classes.lower():
                            remote_testing = True
                        if "adaptive" in classes.lower():
                            adaptive = True

        assessments.append({
            "name": name,
            "url": url,
            "test_types": test_types,
            "remote_testing": remote_testing,
            "adaptive": adaptive,
            "description": "",
            "job_levels": "",
            "languages": "",
            "duration": "",
            "duration_minutes": None,
        })
    return assessments


def get_assessment_details(url):
    html = get_page(url)
    if not html:
        return {}
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    details = {}

    # Description from meta tag (most reliable)
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content", "").strip():
        details["description"] = meta["content"].strip()
    else:
        for p in soup.find_all("p"):
            t = p.get_text(strip=True)
            if len(t) > 80:
                details["description"] = t[:500]
                break

    # Duration: "Approximate Completion Time in minutes = 36"
    m = re.search(r'Approximate Completion Time.*?=\s*(\d+)', page_text, re.I)
    if m:
        details["duration_minutes"] = int(m.group(1))
        details["duration"] = f"{m.group(1)} minutes"
    else:
        m = re.search(r'(\d+)\s*(?:min|mins|minutes)', page_text, re.I)
        if m:
            details["duration_minutes"] = int(m.group(1))
            details["duration"] = f"{m.group(1)} minutes"

    # Job levels (reject "and region." garbage)
    m = re.search(r'Job\s*Levels?\s*[|:]\s*([^\n|]{3,80})', page_text, re.I)
    if m:
        jl = m.group(1).strip()
        if "region" not in jl.lower() and len(jl) > 4:
            details["job_levels"] = jl

    # Languages
    m = re.search(r'Languages?\s*[|:]\s*([^\n|]{2,60})', page_text, re.I)
    if m:
        details["languages"] = m.group(1).strip()

    # Remote testing from detail page
    if re.search(r'remote\s*testing\s*[|:]?\s*yes', page_text, re.I):
        details["remote_testing"] = True

    # Test types from detail page (override catalog if found)
    m = re.search(r'Test\s*Type[s]?\s*[|:]\s*([ABCKPS ]{1,12})', page_text, re.I)
    if m:
        types = split_test_types(m.group(1))
        if types:
            details["test_types"] = types

    return details


def clean_assessment(a):
    """Fix data quality issues in a scraped assessment."""
    # Fix test_types - always split combined strings
    raw = a.get("test_types", [])
    a["test_types"] = split_test_types(raw)

    # Fix bad job_levels
    jl = str(a.get("job_levels", ""))
    if "region" in jl.lower() or len(jl.strip()) < 4:
        a["job_levels"] = ""

    return a


def scrape_full(output_path="data/shl_assessments.json"):
    """Full scrape: catalog pages + detail pages."""
    print("=== Step 1: Scraping catalog pages ===")
    all_items = []
    seen = set()

    for start in range(0, 400, 12):
        url = f"{CATALOG_URL}?start={start}&type=1"
        print(f"Fetching {url}")
        html = get_page(url)
        if not html:
            url2 = f"{CATALOG_URL}?start={start}"
            html = get_page(url2)
        if not html:
            continue

        items = parse_catalog_page(html)
        added = 0
        for item in items:
            if item["url"] not in seen:
                seen.add(item["url"])
                all_items.append(item)
                added += 1

        print(f"  +{added} (total: {len(all_items)})")
        if added == 0 and len(all_items) > 100:
            break
        time.sleep(1)

    print(f"\n=== Step 2: Enriching {len(all_items)} detail pages ===")
    for i, a in enumerate(all_items):
        print(f"  [{i+1}/{len(all_items)}] {a['name'][:55]}")
        details = get_assessment_details(a["url"])
        a.update(details)
        time.sleep(0.5)

    print("\n=== Step 3: Cleaning ===")
    all_items = [clean_assessment(a) for a in all_items]

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

    counts = {}
    for a in all_items:
        for t in a["test_types"]:
            counts[t] = counts.get(t, 0) + 1
    print(f"\n✓ Saved {len(all_items)} assessments → {output_path}")
    print(f"  Type distribution: {counts}")
    return all_items


def fix_existing_json(path):
    """
    Fix an already-scraped JSON without re-scraping.
    Splits 'CPAB' -> ['C','P','A','B'], fixes bad job_levels.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Fixing {len(data)} assessments in {path}...")
    fixed = [clean_assessment(a) for a in data]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(fixed, f, indent=2, ensure_ascii=False)

    counts = {}
    for a in fixed:
        for t in a["test_types"]:
            counts[t] = counts.get(t, 0) + 1

    print(f"✓ Fixed and saved to {path}")
    print(f"  Sample: {fixed[0]['name']} -> test_types: {fixed[0]['test_types']}")
    print(f"  Type distribution: {counts}")
    return fixed


if __name__ == "__main__":
    import sys
    if "--fix-only" in sys.argv:
        path = next((a for a in sys.argv[1:] if not a.startswith("-")), "data/shl_assessments.json")
        fix_existing_json(path)
    else:
        output = next((a for a in sys.argv[1:] if not a.startswith("-")), "data/shl_assessments.json")
        scrape_full(output)
