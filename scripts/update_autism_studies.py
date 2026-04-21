#!/usr/bin/env python3
"""Refresh the JourHelp autism studies feed from PubMed.

The feed intentionally favors research that fits JourHelp's neurodiversity-
affirming support goals: understanding lived experience, accommodations,
sensory needs, masking, burnout, communication, diagnosis, and quality of life.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTFILE = ROOT / "data" / "autism-studies.json"
NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "jourhelp-autism-studies"
EMAIL = "jourhelp@icloud.com"
MAX_ITEMS = 8

AFFIRMING_TERMS = {
    "accommodation": "accommodations",
    "accommodations": "accommodations",
    "autistic adult": "autistic adults",
    "autistic adults": "autistic adults",
    "burnout": "burnout",
    "camouflage": "masking",
    "camouflaging": "masking",
    "communication needs": "communication",
    "diagnostic experience": "diagnosis",
    "diagnostic experiences": "diagnosis",
    "employment": "work and study",
    "identity": "identity",
    "late diagnosis": "late diagnosis",
    "lived experience": "lived experience",
    "lived experiences": "lived experience",
    "masking": "masking",
    "mental health": "mental health",
    "neurodiversity": "neurodiversity",
    "participatory": "participatory research",
    "quality of life": "quality of life",
    "sensory": "sensory needs",
    "self-determination": "self-determination",
    "support needs": "support needs",
    "supported decision": "supported decision-making",
}

EXCLUDED_TERMS = [
    "cure",
    "curing",
    "vaccine",
    "vaccination",
    "prenatal",
    "screening fetus",
    "animal model",
    "mouse model",
    "mice",
    "rat model",
    "maternal infection",
    "biomarker",
    "metabolomic",
    "microbiota",
    "gut-associated",
    "cytokine",
    "genetic risk",
    "risk gene",
    "gene polymorphism",
    "polymorphism",
    "aba",
    "applied behavior analysis",
]

QUERY = """
(
  autism[Title/Abstract] OR autistic[Title/Abstract] OR "autism spectrum disorder"[MeSH Terms]
)
AND
(
  "quality of life"[Title/Abstract] OR sensory[Title/Abstract] OR masking[Title/Abstract]
  OR camouflaging[Title/Abstract] OR burnout[Title/Abstract] OR accommodation*[Title/Abstract]
  OR "support needs"[Title/Abstract] OR "mental health"[Title/Abstract]
  OR "communication needs"[Title/Abstract] OR "late diagnosis"[Title/Abstract]
  OR "diagnostic experience"[Title/Abstract] OR "lived experience"[Title/Abstract]
  OR "autistic adults"[Title/Abstract] OR "autistic people"[Title/Abstract]
  OR neurodiversity[Title/Abstract] OR participatory[Title/Abstract]
  OR employment[Title/Abstract] OR identity[Title/Abstract]
)
NOT
(
  vaccine*[Title/Abstract] OR cure[Title/Abstract] OR prenatal[Title/Abstract]
  OR "animal model"[Title/Abstract] OR mice[Title/Abstract] OR "maternal infection"[Title/Abstract]
  OR "applied behavior analysis"[Title/Abstract] OR metabolomic*[Title/Abstract]
  OR microbiota[Title/Abstract] OR polymorphism*[Title/Abstract] OR biomarker*[Title/Abstract]
)
AND humans[MeSH Terms]
AND english[Language]
""".strip()


def request_text(endpoint: str, params: dict[str, str | int]) -> str:
    params = {**params, "tool": TOOL, "email": EMAIL}
    url = f"{NCBI_BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL}/1.0 ({EMAIL})"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return value


def parse_pub_date(article: ET.Element) -> str:
    date_node = article.find(".//JournalIssue/PubDate")
    if date_node is None:
        return ""
    year = date_node.findtext("Year") or ""
    month = date_node.findtext("Month") or "01"
    day = date_node.findtext("Day") or "01"
    if not year:
        article_date = article.find(".//ArticleDate")
        year = article_date.findtext("Year") if article_date is not None else ""
        month = article_date.findtext("Month") if article_date is not None else month
        day = article_date.findtext("Day") if article_date is not None else day
    if not year:
        return ""
    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }
    month = month_map.get(month[:3].lower(), month.zfill(2) if month.isdigit() else "01")
    day = day.zfill(2) if day.isdigit() else "01"
    return f"{year}-{month}-{day}"


def article_text(article: ET.Element, path: str) -> str:
    node = article.find(path)
    if node is None:
        return ""
    return clean_text(" ".join(node.itertext()))


def article_authors(article: ET.Element) -> str:
    authors = []
    for author in article.findall(".//AuthorList/Author")[:3]:
        last = author.findtext("LastName") or ""
        initials = author.findtext("Initials") or ""
        collective = author.findtext("CollectiveName") or ""
        name = clean_text(collective or f"{last} {initials}")
        if name:
            authors.append(name)
    if not authors:
        return ""
    suffix = " et al." if len(article.findall(".//AuthorList/Author")) > 3 else ""
    return ", ".join(authors) + suffix


def preview_from_abstract(abstract: str) -> str:
    if not abstract:
        return "PubMed record selected by JourHelp's trustworthy-source and topic filters."
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    preview = " ".join(sentences[:2]).strip()
    if len(preview) > 320:
        preview = preview[:317].rstrip() + "..."
    return preview


def score_article(title: str, abstract: str, journal: str) -> tuple[int, list[str]]:
    text = f"{title} {abstract} {journal}".lower()
    if any(term in text for term in EXCLUDED_TERMS):
        return -100, []
    title_text = title.lower()
    if "autism" not in title_text and "autistic" not in title_text:
        return -100, []
    tags = []
    score = 0
    for needle, tag in AFFIRMING_TERMS.items():
        if needle in text:
            score += 2
            if tag not in tags:
                tags.append(tag)
    if "review" in text:
        score += 1
    if "autistic" in text:
        score += 1
    if "participatory" in text or "co-produced" in text:
        score += 2
    return score, tags[:4]


def is_future_publication(value: str) -> bool:
    if not value:
        return False
    try:
        return date.fromisoformat(value) > date.today()
    except ValueError:
        return False


def fetch_pmids() -> list[str]:
    body = request_text(
        "esearch.fcgi",
        {
            "db": "pubmed",
            "term": QUERY,
            "sort": "pub+date",
            "retmode": "json",
            "retmax": 40,
        },
    )
    data = json.loads(body)
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_articles(pmids: list[str]) -> list[dict[str, object]]:
    if not pmids:
        return []
    time.sleep(0.4)
    xml = request_text(
        "efetch.fcgi",
        {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        },
    )
    root = ET.fromstring(xml)
    articles = []
    for record in root.findall(".//PubmedArticle"):
        article = record.find(".//Article")
        if article is None:
            continue
        pmid = record.findtext(".//PMID") or ""
        title = article_text(article, ".//ArticleTitle")
        abstract = article_text(article, ".//Abstract")
        journal = clean_text(article.findtext(".//Journal/Title") or "")
        published = parse_pub_date(article)
        if is_future_publication(published):
            continue
        score, tags = score_article(title, abstract, journal)
        if score < 2:
            continue
        articles.append(
            {
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "authors": article_authors(article),
                "published": published,
                "preview": preview_from_abstract(abstract),
                "tags": tags or ["autism research"],
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "_score": score,
            }
        )
    return sorted(articles, key=lambda item: (item.get("published", ""), item["_score"]), reverse=True)


def write_feed(studies: list[dict[str, object]]) -> None:
    for study in studies:
        study.pop("_score", None)
    payload = {
        "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": "PubMed / NCBI",
        "sourceUrl": "https://pubmed.ncbi.nlm.nih.gov/",
        "method": "Weekly PubMed search for recent peer-reviewed autism research aligned with JourHelp's support, accommodation, sensory, masking, burnout, communication, diagnosis, and quality-of-life goals.",
        "studies": studies[:MAX_ITEMS],
    }
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    OUTFILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        pmids = fetch_pmids()
        studies = fetch_articles(pmids)
        write_feed(studies)
        print(f"Wrote {len(studies[:MAX_ITEMS])} studies to {OUTFILE}")
        return 0
    except Exception as exc:
        fallback = {
            "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source": "PubMed / NCBI",
            "sourceUrl": "https://pubmed.ncbi.nlm.nih.gov/",
            "method": "Feed refresh failed; keeping the section safe and empty until the next weekly run.",
            "studies": [],
            "error": str(exc),
        }
        OUTFILE.parent.mkdir(parents=True, exist_ok=True)
        OUTFILE.write_text(json.dumps(fallback, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Could not refresh studies: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
