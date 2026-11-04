"""
Web Scraper Module
Extracts book information from books.toscrape.com including pagination
and deep product details.
"""

import re
import time
import logging
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any

import requests
from bs4 import BeautifulSoup
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class BookScraper:
    """Scrapes books from books.toscrape.com."""

    BASE_URL = "https://books.toscrape.com/"
    CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-{page}.html"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, request_delay: float = 0.2, timeout: int = 15):
        self.delay = request_delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def _fetch_soup(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch URL content and return parsed BeautifulSoup object."""
        for attempt in range(1, max_retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return BeautifulSoup(response.content, "html.parser")
                elif response.status_code == 404:
                    logger.debug(f"Page not found (404): {url}")
                    return None
                else:
                    logger.warning(f"Status {response.status_code} for {url} (attempt {attempt})")
            except requests.RequestException as e:
                logger.warning(f"Error fetching {url} on attempt {attempt}: {e}")
            time.sleep(self.delay * attempt)
        return None

    def scrape_catalogue_page(self, page_num: int) -> List[Dict[str, Any]]:
        """Scrape items listed on a single catalogue page."""
        url = self.CATALOGUE_URL.format(page=page_num)
        soup = self._fetch_soup(url)
        if not soup:
            return []

        books = []
        product_pods = soup.select("article.product_pod")
        for pod in product_pods:
            try:
                # Title & Relative Link
                title_elem = pod.select_one("h3 a")
                title = title_elem["title"].strip() if title_elem and "title" in title_elem.attrs else ""
                rel_link = title_elem["href"].strip() if title_elem and "href" in title_elem.attrs else ""
                
                # Normalize link
                if rel_link.startswith("catalogue/"):
                    full_link = urljoin(self.BASE_URL, rel_link)
                else:
                    full_link = urljoin(f"{self.BASE_URL}catalogue/", rel_link)

                # Price
                price_elem = pod.select_one(".price_color")
                price_str = price_elem.get_text(strip=True) if price_elem else ""

                # Star Rating class
                rating_elem = pod.select_one("p.star-rating")
                rating_class = [c for c in rating_elem.get("class", []) if c != "star-rating"] if rating_elem else []
                rating_str = rating_class[0] if rating_class else "Unknown"

                # Availability
                avail_elem = pod.select_one(".availability")
                avail_str = avail_elem.get_text(strip=True) if avail_elem else ""

                # Image link
                img_elem = pod.select_one("img.thumbnail")
                img_src = img_elem["src"].strip() if img_elem and "src" in img_elem.attrs else ""
                img_url = urljoin(self.BASE_URL, img_src)

                books.append({
                    "title": title,
                    "price_str": price_str,
                    "rating_str": rating_str,
                    "availability_str": avail_str,
                    "page_number": page_num,
                    "product_url": full_link,
                    "image_url": img_url,
                })
            except Exception as e:
                logger.error(f"Error parsing pod on page {page_num}: {e}")
                continue

        return books

    def scrape_book_details(self, book_meta: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch deep details from the book product page."""
        url = book_meta.get("product_url", "")
        if not url:
            return book_meta

        soup = self._fetch_soup(url)
        if not soup:
            return book_meta

        enriched = dict(book_meta)
        try:
            # Breadcrumbs for category
            breadcrumbs = [a.get_text(strip=True) for a in soup.select("ul.breadcrumb li a")]
            # Format: ['Home', 'Books', 'CategoryName']
            if len(breadcrumbs) >= 3:
                enriched["category"] = breadcrumbs[2]
            else:
                enriched["category"] = "General"

            # Product information table
            info_table = soup.select_one("table.table-striped")
            if info_table:
                for row in info_table.select("tr"):
                    th = row.select_one("th")
                    td = row.select_one("td")
                    if th and td:
                        header = th.get_text(strip=True).lower()
                        value = td.get_text(strip=True)
                        if "upc" in header:
                            enriched["upc"] = value
                        elif "product type" in header:
                            enriched["product_type"] = value
                        elif "price (excl. tax)" in header:
                            enriched["price_excl_tax_str"] = value
                        elif "price (incl. tax)" in header:
                            enriched["price_incl_tax_str"] = value
                        elif "tax" in header:
                            enriched["tax_str"] = value
                        elif "availability" in header:
                            enriched["detail_availability"] = value
                        elif "number of reviews" in header:
                            enriched["reviews_count"] = value

            # Product description
            desc_header = soup.find("div", id="product_description")
            if desc_header:
                desc_p = desc_header.find_next_sibling("p")
                enriched["description"] = desc_p.get_text(strip=True) if desc_p else ""
            else:
                enriched["description"] = ""

        except Exception as e:
            logger.error(f"Error enriching book {url}: {e}")

        return enriched

    def scrape_books(
        self,
        max_pages: Optional[int] = None,
        fetch_details: bool = True,
        max_workers: int = 5
    ) -> pd.DataFrame:
        """
        Scrape books across pages, optionally enriching with product details.
        
        Args:
            max_pages: Maximum number of pages to scrape (1 to 50). If None, scrapes until end.
            fetch_details: Whether to visit individual product pages for extra attributes.
            max_workers: Number of threads for concurrent detail page fetching.
        """
        logger.info(f"Starting catalogue scrape (max_pages={max_pages})...")
        catalogue_items: List[Dict[str, Any]] = []

        page = 1
        while True:
            if max_pages and page > max_pages:
                break
            logger.info(f"Fetching catalogue page {page}...")
            items = self.scrape_catalogue_page(page)
            if not items:
                logger.info(f"No items found on page {page}. Concluding catalogue traversal.")
                break
            catalogue_items.extend(items)
            page += 1
            time.sleep(self.delay)

        total_books = len(catalogue_items)
        logger.info(f"Collected {total_books} items across {page - 1} catalogue pages.")

        if not fetch_details:
            return pd.DataFrame(catalogue_items)

        logger.info(f"Enriching {total_books} books with full details (threads={max_workers})...")
        enriched_items: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_book = {
                executor.submit(self.scrape_book_details, book): book
                for book in catalogue_items
            }
            completed = 0
            for future in as_completed(future_to_book):
                completed += 1
                try:
                    result = future.result()
                    enriched_items.append(result)
                except Exception as exc:
                    original = future_to_book[future]
                    logger.error(f"Book enrichment generated exception for '{original.get('title')}': {exc}")
                    enriched_items.append(original)

                if completed % 50 == 0 or completed == total_books:
                    logger.info(f"Progress: {completed}/{total_books} books detailed ({completed/total_books*100:.1f}%)")

        logger.info("Scraping completed successfully.")
        return pd.DataFrame(enriched_items)
