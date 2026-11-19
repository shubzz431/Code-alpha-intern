"""
CodeAlpha Data Analytics Internship
Task 3: Data Visualization (Simple & Clean)

This script loads the books dataset, creates 4 simple visual charts,
and saves them directly into the 'charts/' folder.
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")
os.environ["MPLCONFIGDIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mpl_config")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean visual theme
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10})

# Create charts directory if it doesn't exist
os.makedirs("charts", exist_ok=True)

print("=" * 60)
print("   TASK 3: DATA VISUALIZATION - SIMPLE & FAST PIPELINE   ")
print("=" * 60)

# Step 1: Load the Dataset
data_file = "books_data.csv"
print(f"\n[1/5] Loading data from '{data_file}'...")
df = pd.read_csv(data_file)
print(f"-> Successfully loaded {len(df)} books!")

# Step 2: Chart 1 - Top 10 Book Categories (Bar Chart)
print("\n[2/5] Creating Chart 1: Top 10 Book Categories...")
top_cats = df["category"].value_counts().head(10)

plt.figure(figsize=(9, 5))
bars = plt.barh(top_cats.index[::-1], top_cats.values[::-1], color="#3b82f6", edgecolor="black")
plt.title("Top 10 Book Categories by Count", fontsize=14, fontweight="bold")
plt.xlabel("Number of Books")
plt.ylabel("Category")

# Add count numbers on each bar
for bar in bars:
    w = bar.get_width()
    plt.text(w + 1, bar.get_y() + bar.get_height()/2, f"{int(w)}", va="center", fontweight="bold")

plt.tight_layout()
plt.savefig("charts/1_top_categories.png", dpi=200)
plt.close()
print("-> Saved: charts/1_top_categories.png")

# Step 3: Chart 2 - Book Price Distribution (Histogram)
print("\n[3/5] Creating Chart 2: Book Price Distribution...")
plt.figure(figsize=(9, 5))
plt.hist(df["price_gbp"], bins=20, color="#10b981", edgecolor="black", alpha=0.8)

# Add average price line
avg_price = df["price_gbp"].mean()
plt.axvline(avg_price, color="red", linestyle="--", linewidth=2, label=f"Average Price (£{avg_price:.2f})")

plt.title("Distribution of Book Prices (£ GBP)", fontsize=14, fontweight="bold")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.legend()
plt.tight_layout()
plt.savefig("charts/2_price_distribution.png", dpi=200)
plt.close()
print("-> Saved: charts/2_price_distribution.png")

# Step 4: Chart 3 - Customer Rating Share (Pie Chart)
print("\n[4/5] Creating Chart 3: Star Rating Share...")
rating_counts = df["rating"].value_counts().sort_index()

plt.figure(figsize=(7, 7))
colors = ["#f87171", "#fb923c", "#facc15", "#60a5fa", "#4ade80"]
labels = [f"{r} Star ({cnt})" for r, cnt in rating_counts.items()]

plt.pie(
    rating_counts.values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
plt.title("Customer Star Rating Breakdown (1 to 5 Stars)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/3_rating_pie_chart.png", dpi=200)
plt.close()
print("-> Saved: charts/3_rating_pie_chart.png")

# Step 5: Chart 4 - Price vs Star Rating (Box Plot)
print("\n[5/5] Creating Chart 4: Price vs Star Rating...")
plt.figure(figsize=(9, 5))
sns.boxplot(
    data=df,
    x="rating",
    y="price_gbp",
    hue="rating",
    palette="Set2",
    legend=False
)
plt.title("Book Prices across Customer Star Ratings", fontsize=14, fontweight="bold")
plt.xlabel("Star Rating (1 to 5)")
plt.ylabel("Price (£ GBP)")
plt.tight_layout()
plt.savefig("charts/4_price_by_rating.png", dpi=200)
plt.close()
print("-> Saved: charts/4_price_by_rating.png")

print("\n" + "=" * 60)
print("SUCCESS: All 4 charts have been created in the 'charts/' folder!")
print("=" * 60)
