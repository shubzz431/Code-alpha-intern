# Task 1: Web Scraping & Exploratory Data Analysis

Part of the **CodeAlpha Data Analytics Internship** program.

---

## 📌 Project Overview

This project implements an end-to-end web scraping, data engineering, and exploratory analytics pipeline targeting the e-commerce catalog at [Books to Scrape](https://books.toscrape.com). 

The goal is to automatically extract structured book data across multiple catalog pages, enrich each record with deep product details (UPC, tax, exact stock quantity, categories, descriptions), clean and validate the dataset, and generate exploratory data visualizations and audit metrics.

---

## 🏗️ Architecture & Pipeline Workflow

```
                                  +------------------------+
                                  | books.toscrape.com     |
                                  | (50 Catalogue Pages)   |
                                  +-----------+------------+
                                              |
                                              v
+-----------------------+         +-----------+------------+
|  BookScraper (src)    |<--------|  Catalogue & Detail    |
|  - requests           |         |  HTML Parsing (BS4)    |
|  - ThreadPoolExecutor |         +-----------+------------+
+-----------+-----------+                     |
            |                                 v
            |                      data/raw/books_raw.csv
            v
+-----------+-----------+
|  DataCleaner (src)    |--------> data/processed/books_cleaned.csv
|  - currency parsing   |--------> data/processed/books_cleaned.json
|  - rating & stock int |
|  - deduplication      |
+-----------+-----------+
            |
            v
+-----------+-----------+
|  DataAnalyzer (src)   |--------> output/scraping_summary_report.txt
|  - price distribution |--------> output/figures/*.png
|  - rating & category  |
+-----------------------+
```

---

## 📁 Repository Structure

```
Task_1_Web_Scraping/
├── data/
│   ├── raw/
│   │   └── books_raw.csv            # Raw scraped data (1,000 records)
│   └── processed/
│       ├── books_cleaned.csv        # Cleaned, standardized CSV
│       └── books_cleaned.json       # Cleaned JSON format for analytics
├── notebooks/
│   └── Task1_Web_Scraping_Demo.ipynb# Interactive Jupyter Notebook
├── output/
│   ├── figures/
│   │   ├── price_distribution.png   # Price histogram & mean/median
│   │   ├── rating_distribution.png  # Customer star rating distribution
│   │   ├── top_categories.png       # Top 10 categories by volume
│   │   ├── price_by_rating.png      # Price variations across ratings
│   │   └── category_avg_price.png   # Top categories by average price
│   └── scraping_summary_report.txt  # Textual summary metrics & audit
├── src/
│   ├── __init__.py
│   ├── scraper.py                   # Multi-threaded web scraper
│   ├── data_cleaner.py              # Data cleaning and type conversions
│   └── analysis.py                  # EDA plotting & report generation
├── main.py                          # Unified CLI entry point
└── README.md                        # Documentation
```

---

## 📊 Dataset Schema & Data Dictionary

| Column Name | Data Type | Description |
|:---|:---|:---|
| `upc` | `str` | Unique Product Code / Universal Product Code |
| `title` | `str` | Full title of the book |
| `category` | `str` | Book genre/category derived from breadcrumbs |
| `price_gbp` | `float` | Base book price in Great British Pounds (£) |
| `price_excl_tax_gbp` | `float` | Product price excluding tax |
| `price_incl_tax_gbp` | `float` | Product price including tax |
| `tax_gbp` | `float` | Applicable tax amount |
| `star_rating` | `int` | Customer rating mapped to integer (1 to 5) |
| `is_in_stock` | `bool` | Stock availability flag (`True` / `False`) |
| `stock_quantity` | `int` | Exact inventory units available |
| `reviews_count` | `int` | Number of customer reviews |
| `description` | `str` | Product synopsis/description text |
| `product_url` | `str` | Canonical product detail URL |
| `image_url` | `str` | Direct link to high-resolution product cover image |
| `page_number` | `int` | Catalogue pagination page index |

---

## 📈 Key Findings & Insights

Based on the complete scrape of all **1,000 books** across **50 categories**:

1. **Pricing Structure**:
   - **Mean Price**: £35.07
   - **Median Price**: £35.98
   - **Standard Deviation**: £14.45
   - Prices range evenly from £10.00 to £59.99 without severe extreme outliers.
2. **Inventory & Availability**:
   - Total catalog inventory is **8,585 units**.
   - 100% of books in the catalog currently have positive stock (`is_in_stock = True`).
3. **Rating Distribution**:
   - Ratings are remarkably uniform across all 5 tiers:
     - 1 Star: 226 books (22.6%)
     - 2 Stars: 196 books (19.6%)
     - 3 Stars: 203 books (20.3%)
     - 4 Stars: 179 books (17.9%)
     - 5 Stars: 196 books (19.6%)
   - Overall mean rating: **2.92 / 5.0**.
4. **Category Volume**:
   - Top genres by book count: *Default* (152), *Nonfiction* (110), *Sequential Art* (75), *Add a comment* (67), and *Fiction* (65).

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 2. Run the Full Scraping Pipeline
```bash
# Scrape all 50 catalogue pages (1,000 books with multithreading)
python main.py --pages 50 --workers 12

# Or run a quick 5-page sample (100 books)
python main.py --pages 5 --workers 8
```

### 3. Open Interactive Notebook
Open `notebooks/Task1_Web_Scraping_Demo.ipynb` in VS Code or Jupyter Lab to inspect data interactively.
