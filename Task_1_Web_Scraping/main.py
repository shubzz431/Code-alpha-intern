"""
Task 1: Web Scraping Pipeline Runner
Orchestrates scraping, data cleaning, exporting, and exploratory data analysis.

Usage:
    python main.py --pages 5
    python main.py --pages 50 --workers 10
"""

import os
import sys
import argparse
import logging
import time

# Ensure src modules are resolvable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from src.scraper import BookScraper
from src.data_cleaner import DataCleaner
from src.analysis import DataAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Pipeline")


def parse_args():
    parser = argparse.ArgumentParser(
        description="CodeAlpha Data Analytics - Task 1: Web Scraping Pipeline"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=5,
        help="Number of catalogue pages to scrape (1 to 50). 20 books per page. Default is 5 (100 books)."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of concurrent worker threads for detail page scraping. Default is 8."
    )
    parser.add_argument(
        "--skip-details",
        action="store_true",
        help="Skip fetching deep product details (faster, but extracts fewer attributes)."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    start_time = time.time()

    base_dir = CURRENT_DIR
    data_dir = os.path.join(base_dir, "data")
    raw_path = os.path.join(data_dir, "raw", "books_raw.csv")
    cleaned_csv_path = os.path.join(data_dir, "processed", "books_cleaned.csv")
    cleaned_json_path = os.path.join(data_dir, "processed", "books_cleaned.json")
    output_dir = os.path.join(base_dir, "output")

    logger.info("=" * 65)
    logger.info("   CODEALPHA DATA ANALYTICS INTERNSHIP: TASK 1 (WEB SCRAPING)   ")
    logger.info("=" * 65)
    logger.info(f"Target: books.toscrape.com | Pages: {args.pages} | Workers: {args.workers}")

    # Step 1: Scrape Data
    logger.info("\n--- STEP 1: SCRAPING WEB DATA ---")
    scraper = BookScraper()
    raw_df = scraper.scrape_books(
        max_pages=args.pages,
        fetch_details=not args.skip_details,
        max_workers=args.workers
    )

    if raw_df.empty:
        logger.error("No books were scraped. Aborting pipeline.")
        sys.exit(1)

    logger.info(f"Scraped {len(raw_df)} raw records.")

    # Step 2: Clean & Validate Data
    logger.info("\n--- STEP 2: DATA CLEANING & VALIDATION ---")
    cleaned_df = DataCleaner.clean_dataframe(raw_df)
    DataCleaner.save_datasets(
        raw_df=raw_df,
        cleaned_df=cleaned_df,
        raw_path=raw_path,
        processed_csv_path=cleaned_csv_path,
        processed_json_path=cleaned_json_path
    )

    # Step 3: Exploratory Analysis & Visualization
    logger.info("\n--- STEP 3: EXPLORATORY DATA ANALYSIS & VISUALIZATION ---")
    analyzer = DataAnalyzer(cleaned_df, output_dir=output_dir)
    analyzer.run_all()

    elapsed = time.time() - start_time
    logger.info("\n" + "=" * 65)
    logger.info(f"PIPELINE COMPLETED SUCCESSFULLY in {elapsed:.2f} seconds!")
    logger.info(f"Raw Data:         {raw_path}")
    logger.info(f"Cleaned CSV:      {cleaned_csv_path}")
    logger.info(f"Cleaned JSON:     {cleaned_json_path}")
    logger.info(f"Report & Charts:  {output_dir}")
    logger.info("=" * 65)


if __name__ == "__main__":
    main()
