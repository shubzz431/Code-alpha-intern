# CodeAlpha_BookEDA

**CodeAlpha Data Analytics Internship, Task 2: Exploratory Data Analysis (EDA)**

A complete EDA project on a dataset of about 1000 books. A small web scraper collects the data from [books.toscrape.com](https://books.toscrape.com) (a practice website built for learning scraping), and a Jupyter notebook explores it: it asks questions first, checks the data quality, looks for patterns and unusual values, and tests four hypotheses with statistics.

## What the notebook covers

| Task 2 requirement | Where in `EDA_Books.ipynb` |
|---|---|
| Ask meaningful questions before analysis | Step 1: six questions turned into four hypotheses |
| Explore the data structure, variables and data types | Step 3 |
| Detect data issues and problems | Step 4: missing values, duplicates, constant columns, placeholder categories, impossible values, extreme prices (IQR rule) |
| Identify trends, patterns and anomalies | Steps 5, 6 and 8: 7 charts, correlation matrix, outlier tables |
| Test hypotheses and validate assumptions | Step 7: normality check, then Spearman, Kruskal-Wallis and Chi-square tests with effect sizes and a multiple-testing correction |

## Hypotheses tested

| | Null hypothesis | Test |
|---|---|---|
| H1 | Price and star rating are not related | Spearman correlation |
| H2 | Average price is the same in every category | Kruskal-Wallis |
| H3 | All star ratings are equally common | Chi-square goodness of fit |
| H4 | Description length and star rating are not related | Spearman correlation |

The notebook ends with an automatic **Summary of findings** (Step 9), built from the computed results, and saves a cleaned dataset.

## Dataset columns

`title`, `category`, `price_gbp`, `rating` (1 to 5), `in_stock`, `units_available`, `num_reviews`, `upc`, `description`, `product_url`

## How to run

```bash
pip install -r requirements.txt

python scraper.py        # collects the data and creates books.csv (about 5 to 10 minutes)
jupyter notebook         # open EDA_Books.ipynb and click "Run All"
```

Quick test of the scraper: `python scraper.py --max-pages 2`

## Project structure

```
CodeAlpha_BookEDA/
├── scraper.py           # collects the data -> books.csv
├── EDA_Books.ipynb      # the full analysis
├── books.csv            # raw data (created by scraper.py)
├── books_clean.csv      # cleaned data (created by the notebook)
├── charts/              # 7 PNG charts (created by the notebook)
├── requirements.txt
└── README.md
```

## Responsible scraping

The scraper only visits a website that exists for practice. It waits between requests, identifies itself with a User-Agent, and retries gently instead of hammering the server.

## Tools

Python, Requests, BeautifulSoup4, Pandas, NumPy, SciPy, Matplotlib, Jupyter

## Notes and limits

- The data comes from a practice website, so its patterns may not match real bookshops.
- It is a single snapshot with no dates, so trends over time cannot be studied.
- Correlation does not prove causation.

---
*Built as part of the CodeAlpha Data Analytics Internship.*
