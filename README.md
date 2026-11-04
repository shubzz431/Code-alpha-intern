# CodeAlpha Data Analytics Internship Projects

Welcome to the official repository for the **CodeAlpha Data Analytics Internship** program. This repository houses the projects, source code, datasets, and analysis reports completed as part of the internship curriculum.

---

## 📌 Internship Task Tracker

| Task | Domain | Focus Area | Status | Directory |
|:---:|:---|:---|:---:|:---|
| **Task 1** | **Web Scraping** | Multi-page data extraction, cleaning, and EDA | ✅ Completed | [`Task_1_Web_Scraping/`](Task_1_Web_Scraping/) |
| **Task 2** | Exploratory Data Analysis (EDA) | Statistical hypotheses, data issues, trend discovery | ⏳ Ready | `Task_2_EDA/` |
| **Task 3** | Data Visualization | Compelling visual storytelling, Matplotlib/Seaborn dashboards | ⏳ Ready | `Task_3_Data_Visualization/` |
| **Task 4** | Sentiment Analysis | NLP sentiment classification and opinion mining | ⏳ Ready | `Task_4_Sentiment_Analysis/` |

---

## 🚀 Task 1: Web Scraping & Dataset Creation (Completed)

### Summary
Built a robust, multi-threaded web scraping pipeline using Python, `BeautifulSoup4`, `requests`, and `pandas` to extract, clean, and analyze an e-commerce catalog of 1,000 books from [Books to Scrape](https://books.toscrape.com).

### Highlights:
- **Comprehensive Data Extraction**: Scraped 50 catalog pages + deep product detail pages for 1,000 books.
- **Enriched Attributes**: Captured UPC, title, category, price (£), price excl/incl tax, tax, rating (1-5), availability, stock quantity, customer reviews count, and descriptions.
- **Production-Grade Data Pipeline**:
  - Handles network failures, retry backoffs, and concurrency via `ThreadPoolExecutor`.
  - Cleans currencies, standardizes ratings, parses stock counts, and eliminates duplicates.
  - Exports to both CSV and JSON formats.
- **Exploratory Visualizations**:
  - `price_distribution.png`: Histogram & mean/median price markers.
  - `rating_distribution.png`: Customer star rating breakdown.
  - `top_categories.png`: Top 10 categories by volume.
  - `price_by_rating.png`: Price variations across star ratings.
  - `category_avg_price.png`: Average price per category.
- **Interactive Notebook**: `Task1_Web_Scraping_Demo.ipynb` for quick inspection in VS Code.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/CodeAlpha_DataAnalytics.git
   cd CodeAlpha_DataAnalytics
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Task 1 Pipeline:**
   ```bash
   python Task_1_Web_Scraping/main.py --pages 50 --workers 12
   ```

---

## 📋 CodeAlpha Submission Checklist

- [x] Web scraping pipeline implemented with Python & BeautifulSoup
- [x] Multi-page navigation & HTML parsing implemented
- [x] Raw and cleaned datasets generated in `data/raw/` and `data/processed/`
- [x] Automated data cleaning and validation
- [x] Exploratory charts & summary audit report generated in `output/`
- [x] Modular project architecture with reproducible commands
- [x] Comprehensive documentation and README
- [ ] Push repository to GitHub (`CodeAlpha_ProjectName`)
- [ ] Share video explanation and repo link on LinkedIn tagging `@CodeAlpha`
- [ ] Submit form via the official CodeAlpha portal

---

## 👨‍💻 Author
**CodeAlpha Data Analytics Intern**  
Connect on [LinkedIn](https://www.linkedin.com/)
