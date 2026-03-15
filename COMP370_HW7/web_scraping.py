#!/usr/bin/env python3

import argparse
import json
import re
import time
from typing import List, Dict, Optional

import requests
import requests_cache
from bs4 import BeautifulSoup

HOMEPAGE = "https://montrealgazette.com/category/news/"

HEADERS = {
    "User-Agent": "COMP370-Homework-Scraper/1.0 (+for academic use; contact if issues)"
}

REQUEST_DELAY = 1.0

def fetch(url: str) -> requests.Response:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp

def discover_trending_article_urls(home_html: str) -> List[str]:
    soup = BeautifulSoup(home_html, "html.parser")

    candidates = []
    for h in soup.find_all(["h2", "h3", "h4"], string=True):
        if h.get_text(strip=True).lower() == "trending":
            container = h.parent
            if container:
                links = container.find_all("a", href=True)
                for a in links:
                    href = a["href"]
                    if is_probable_article_url(href):
                        candidates.append(normalize_url(href))
            if len(candidates) >= 5:
                break

    if len(candidates) < 5:
        seen = set(candidates)
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if is_probable_article_url(href):
                url = normalize_url(href)
                if url not in seen:
                    candidates.append(url)
                    seen.add(url)
            if len(candidates) >= 5:
                break

    return candidates[:5]

def is_probable_article_url(url: str) -> bool:
    if not url:
        return False
    bad_patterns = ["/category/", "/tag/", "/topics/", "/author/", "/about", "#", "javascript:"]
    if any(p in url for p in bad_patterns):
        return False
    return True

def normalize_url(href: str) -> str:
    if href.startswith("http"):
        return href
    return f"https://montrealgazette.com{href if href.startswith('/') else '/' + href}"

def extract_from_jsonld(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    data = {"title": None, "publication_date": None, "author": None, "blurb": None}
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            parsed = json.loads(script.string or "{}")
        except Exception:
            continue

        def first_news_article(obj):
            if isinstance(obj, dict) and obj.get("@type") in ("NewsArticle", "Article"):
                return obj
            if isinstance(obj, list):
                for item in obj:
                    hit = first_news_article(item)
                    if hit:
                        return hit
            if isinstance(obj, dict):
                for v in obj.values():
                    hit = first_news_article(v)
                    if hit:
                        return hit
            return None

        art = first_news_article(parsed)
        if art:
            data["title"] = data["title"] or art.get("headline") or art.get("name")
            data["publication_date"] = data["publication_date"] or art.get("datePublished") or art.get("dateModified")
            author = art.get("author")
            if isinstance(author, dict):
                data["author"] = data["author"] or author.get("name")
            elif isinstance(author, list) and author:
                names = [a.get("name") for a in author if isinstance(a, dict) and a.get("name")]
                if names:
                    data["author"] = data["author"] or ", ".join(names)
            data["blurb"] = data["blurb"] or art.get("description")
            break
    return data

def extract_from_meta(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    def meta(name=None, prop=None):
        if name:
            m = soup.find("meta", attrs={"name": name})
            if m and m.get("content"):
                return m["content"].strip()
        if prop:
            m = soup.find("meta", attrs={"property": prop})
            if m and m.get("content"):
                return m["content"].strip()
        return None

    title = (meta(prop="og:title") or
             meta(name="twitter:title") or
             (soup.find("h1").get_text(strip=True) if soup.find("h1") else None))

    publication_date = (meta(prop="article:published_time") or
                        meta(name="pubdate") or
                        meta(name="date"))

    author = (meta(name="author") or
              (soup.find(attrs={"class": re.compile(r"byline|author", re.I)}) or {}).get_text(strip=True)
              if soup.find(attrs={"class": re.compile(r"byline|author", re.I)}) else None)

    blurb = (meta(name="description") or
             meta(prop="og:description") or
             meta(name="twitter:description"))

    return {
        "title": title,
        "publication_date": publication_date,
        "author": author,
        "blurb": blurb,
    }

def clean_whitespace(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    return re.sub(r"\s+", " ", s).strip()

def extract_article_fields(html: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "html.parser")
    data = extract_from_jsonld(soup)

    meta_data = extract_from_meta(soup)
    for k in ["title", "publication_date", "author", "blurb"]:
        if not data.get(k):
            data[k] = meta_data.get(k)

    for k in data:
        data[k] = clean_whitespace(data[k])

    return data

def main():
    parser = argparse.ArgumentParser(description="Collect 5 trending Montreal Gazette stories.")
    parser.add_argument("-o", "--output", required=True, help="Path to JSON output (e.g., trending.json)")
    parser.add_argument("--homepage", default=HOMEPAGE, help="Override the discovery page URL.")
    parser.add_argument("--expire-hours", type=int, default=6, help="Cache expiry in hours.")
    parser.add_argument("--no-cache", action="store_true", help="Disable requests caching.")
    args = parser.parse_args()

    if not args.no_cache:
        requests_cache.install_cache("mg_trending_cache", expire_after=args.expire_hours * 3600)

    home_resp = fetch(args.homepage)
    urls = discover_trending_article_urls(home_resp.text)

    results: List[Dict[str, Optional[str]]] = []
    for url in urls:
        try:
            time.sleep(REQUEST_DELAY)
            r = fetch(url)
            fields = extract_article_fields(r.text)
            fields = {
                "title": fields.get("title"),
                "publication_date": fields.get("publication_date"),
                "author": fields.get("author"),
                "blurb": fields.get("blurb"),
            }
            results.append(fields)
        except Exception as e:
            results.append({
                "title": None,
                "publication_date": None,
                "author": None,
                "blurb": None,
            })

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
