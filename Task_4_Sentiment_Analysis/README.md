# CodeAlpha Data Analytics Internship – Task 4
## Sentiment Analysis

### Project Overview
This project analyzes customer product reviews using Natural Language Processing (NLP) and VADER Sentiment Analysis. Reviews are classified into three categories: Positive, Negative, and Neutral.

### Dataset
- File: `reviews.csv`
- Total reviews: 100
- Main columns: `review_id`, `product`, `rating`, and `review_text`

### Tools and Libraries
- Python
- Pandas
- Matplotlib
- Seaborn
- VADER Sentiment
- WordCloud

### Methodology
1. Load customer reviews from the CSV file.
2. Analyze review text using VADER.
3. Calculate compound sentiment scores.
4. Classify reviews as Positive, Negative, or Neutral.
5. Export the analyzed data to `analyzed_reviews.csv`.
6. Generate visualizations to understand sentiment patterns.

### Results
| Sentiment | Reviews | Percentage |
|---|---:|---:|
| Positive | 66 | 66% |
| Negative | 28 | 28% |
| Neutral | 6 | 6% |
| **Total** | **100** | **100%** |

### Visualizations
Four charts are generated:

1. `1_sentiment_counts.png` – Overall sentiment distribution.
2. `2_rating_vs_sentiment.png` – Star rating compared with sentiment score.
3. `3_wordcloud.png` – Most common words in customer reviews.
4. `4_product_sentiment.png` – Sentiment distribution across products.

### How to Run
1. Install the required libraries:

   ```bash
   pip install pandas matplotlib seaborn vaderSentiment wordcloud
   ```

2. Make sure `reviews.csv` and `main.py` are in the same folder.
3. Run the script:

   ```bash
   python main.py
   ```

4. The analyzed CSV file and charts will be generated automatically.

### Conclusion
The analysis found that 66% of the supplied customer reviews were positive, 28% were negative, and 6% were neutral. The visualizations help compare customer opinions across products and identify common themes in the reviews.

*Note: VADER performs lexicon-based sentiment polarity analysis. It does not independently identify specific emotions such as anger, sadness, or happiness.*