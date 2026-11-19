"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping
Project: Book Market Scraper

Scrapes every book from https://books.toscrape.com (a practice website made
for learning web scraping) and builds a clean dataset saved as a CSV file.

Usage:
    python scraper.py                  # full run (~1000 books, with detail pages)
    python scraper.py --no-details     # fast run (listing pages only)
    python scraper.py --max-pages 2    # quick test run
"""

import argparse
import csv
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational project; CodeAlpha internship)"}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

FIELDS = [
    "title",
    "category",
    "price_gbp",
    "rating",
    "in_stock",
    "units_available",
    "num_reviews",
    "upc",
    "description",
    "product_url",
]

log = logging.getLogger("scraper")


# ---------- Helpers ----------

def make_session():
    """A requests session that retries automatically if the server hiccups."""
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


def get_soup(session, url):
    """Download a page and turn it into a BeautifulSoup object."""
    response = session.get(url, timeout=15)
    response.raise_for_status()
    # .content (bytes) lets BeautifulSoup detect UTF-8 correctly (avoids "Â£" glitches)
    return BeautifulSoup(response.content, "html.parser")


def to_price(text):
    """'£51.77' -> 51.77"""
    return float(re.sub(r"[^\d.]", "", text))


# ---------- Parsing ----------

def parse_listing_page(soup, page_url):
    """Extract the basic info of every book card on a listing page."""
    books = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        rating_class = next(c for c in card.select_one("p.star-rating")["class"] if c != "star-rating")
        books.append(
            {
                "title": link["title"],
                "price_gbp": to_price(card.select_one("p.price_color").get_text()),
                "rating": RATINGS.get(rating_class),
                "in_stock": "in stock" in card.select_one("p.availability").get_text().lower(),
                "product_url": urljoin(page_url, link["href"]),
            }
        )
    return books


def next_page_url(soup, page_url):
    """Return the URL of the next page, or None on the last page."""
    nxt = soup.select_one("li.next a")
    return urljoin(page_url, nxt["href"]) if nxt else None


def parse_detail_page(soup):
    """Extract extra info from a single book's page."""
    crumbs = soup.select("ul.breadcrumb li a")  # Home > Books > Category
    table = {
        row.th.get_text(strip=True): row.td.get_text(strip=True)
        for row in soup.select("table.table-striped tr")
    }
    stock_match = re.search(r"\((\d+) available\)", table.get("Availability", ""))

    description = None
    header = soup.select_one("#product_description")
    if header:
        paragraph = header.find_next_sibling("p")
        description = paragraph.get_text(strip=True) if paragraph else None

    return {
        "category": crumbs[-1].get_text(strip=True) if crumbs else None,
        "upc": table.get("UPC"),
        "units_available": int(stock_match.group(1)) if stock_match else 0,
        "num_reviews": int(table.get("Number of reviews", 0)),
        "description": description,
    }


# ---------- Main scraping flow ----------

def scrape(max_pages=None, details=True, delay=0.3):
    session = make_session()
    books, url, page_no = [], START_URL, 0

    # Step 1: walk through every listing page (pagination)
    while url and (max_pages is None or page_no < max_pages):
        page_no += 1
        soup = get_soup(session, url)
        found = parse_listing_page(soup, url)
        books.extend(found)
        log.info("Listing page %d: %d books (total %d)", page_no, len(found), len(books))
        url = next_page_url(soup, url)
        time.sleep(delay)  # be polite to the server

    # Step 2: open each book's own page for the extra details
    if details:
        for i, book in enumerate(books, 1):
            try:
                book.update(parse_detail_page(get_soup(session, book["product_url"])))
            except requests.RequestException as exc:
                log.warning("Skipping details for '%s': %s", book["title"], exc)
            if i % 50 == 0:
                log.info("Detail pages done: %d/%d", i, len(books))
            time.sleep(delay)

    # Step 3: remove duplicates (same product page seen twice)
    unique = {book["product_url"]: book for book in books}
    return list(unique.values())


def save_csv(books, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig so the file opens correctly in Excel
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore", restval="")
        writer.writeheader()
        writer.writerows(books)
    log.info("Saved %d books to %s", len(books), path)


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com into a CSV dataset.")
    parser.add_argument("--max-pages", type=int, default=None, help="stop after N listing pages (for testing)")
    parser.add_argument("--no-details", action="store_true", help="skip individual book pages (faster)")
    parser.add_argument("--delay", type=float, default=0.3, help="seconds to wait between requests")
    parser.add_argument("--output", default="books.csv", help="where to save the CSV")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
    books = scrape(max_pages=args.max_pages, details=not args.no_details, delay=args.delay)
    save_csv(books, args.output)


if __name__ == "__main__":
    main()
