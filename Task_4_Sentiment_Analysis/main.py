
"""
CodeAlpha Data Analytics Internship
Task 4: Sentiment Analysis (Simple & Clean)

This script analyzes customer reviews using VADER Sentiment Analysis,
classifies them into Positive, Neutral, or Negative, and creates 4 visual charts.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

# Set a clean visual theme
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10})

# Create charts directory if it doesn't exist
os.makedirs("charts", exist_ok=True)

print("=" * 60)
print("   TASK 4: SENTIMENT ANALYSIS - SIMPLE & FAST PIPELINE   ")
print("=" * 60)

# Step 1: Load Reviews Data
data_file = "reviews.csv"
print(f"\n[1/6] Loading reviews from '{data_file}'...")
df = pd.read_csv(data_file)
print(f"-> Successfully loaded {len(df)} customer reviews!")

# Step 2: Calculate Sentiment Scores using VADER
print("\n[2/6] Analyzing sentiment for each review...")
analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text):
    scores = analyzer.polarity_scores(str(text))
    compound = scores["compound"]

    if compound >= 0.05:
        category = "Positive"
    elif compound <= -0.05:
        category = "Negative"
    else:
        category = "Neutral"

    return compound, category


results = df["review_text"].apply(get_sentiment)
df["sentiment_score"] = [r[0] for r in results]
df["sentiment"] = [r[1] for r in results]

# Save analyzed data to a new clean CSV
df.to_csv("analyzed_reviews.csv", index=False)
print("-> Saved analyzed data to: analyzed_reviews.csv")

# Print summary counts
counts = df["sentiment"].value_counts()

print("\nSentiment Results:")
for cat, cnt in counts.items():
    print(f"   * {cat:8s}: {cnt:3d} reviews ({cnt/len(df)*100:.1f}%)")

# Step 3: Chart 1 - Sentiment Distribution Bar Chart
print("\n[3/6] Creating Chart 1: Sentiment Distribution...")

plt.figure(figsize=(8, 4.5))

colors = {
    "Positive": "#10b981",
    "Neutral": "#64748b",
    "Negative": "#ef4444"
}

bar_colors = [colors.get(c, "#3b82f6") for c in counts.index]

bars = plt.bar(
    counts.index,
    counts.values,
    color=bar_colors,
    edgecolor="black",
    width=0.55
)

for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h + 1,
        f"{int(h)} ({h/len(df)*100:.1f}%)",
        ha="center",
        fontweight="bold"
    )

plt.title("Customer Sentiment Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Sentiment Category")
plt.ylabel("Number of Reviews")
plt.ylim(0, max(counts.values) * 1.20)
plt.tight_layout()
plt.savefig("charts/1_sentiment_counts.png", dpi=200)
plt.close()

print("-> Saved: charts/1_sentiment_counts.png")

# Step 4: Chart 2 - Star Rating vs Sentiment Score
print("\n[4/6] Creating Chart 2: Rating vs Sentiment Score...")

plt.figure(figsize=(8, 4.5))

sns.boxplot(
    data=df,
    x="rating",
    y="sentiment_score",
    hue="rating",
    palette="RdYlGn",
    legend=False
)

plt.axhline(
    0,
    color="gray",
    linestyle="--",
    linewidth=1.5,
    label="Neutral Threshold"
)

plt.title(
    "Correlation: Customer Star Rating vs Sentiment Score",
    fontsize=14,
    fontweight="bold"
)
plt.xlabel("Star Rating (1 to 5)")
plt.ylabel("Sentiment Score (-1.0 Negative to +1.0 Positive)")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("charts/2_rating_vs_sentiment.png", dpi=200)
plt.close()

print("-> Saved: charts/2_rating_vs_sentiment.png")

# Step 5: Chart 3 - Word Cloud of Customer Reviews
print("\n[5/6] Creating Chart 3: Word Cloud...")

all_text = " ".join(df["review_text"].dropna())

wc = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",
    max_words=60
).generate(all_text)

plt.figure(figsize=(9, 4.5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Most Common Words in Customer Reviews", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/3_wordcloud.png", dpi=200)
plt.close()

print("-> Saved: charts/3_wordcloud.png")

# Step 6: Chart 4 - Product-wise Sentiment Distribution
print("\n[6/6] Creating Chart 4: Product-wise Sentiment Distribution...")

sentiment_order = ["Negative", "Neutral", "Positive"]

product_sentiment = (
    df.groupby(["product", "sentiment"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=sentiment_order, fill_value=0)
)

product_sentiment.plot(
    kind="bar",
    figsize=(11, 6),
    color=["#ef4444", "#64748b", "#10b981"],
    edgecolor="black"
)

plt.title("Product-wise Sentiment Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Product")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=35, ha="right")
plt.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("charts/4_product_sentiment.png", dpi=200)
plt.close()

print("-> Saved: charts/4_product_sentiment.png")

# Final Success Message
print("\n" + "=" * 60)
print("SUCCESS: All 4 charts and analyzed_reviews.csv are ready!")
print("=" * 60)
