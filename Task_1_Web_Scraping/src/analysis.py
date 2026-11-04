"""
Exploratory Data Analysis and Visualization Module
Generates statistical reports and analytical charts from the cleaned dataset.
"""

import os
import logging
from typing import Dict, Any
import pandas as pd
import numpy as np
import matplotlib
# Use Agg backend for headless / server script execution
matplotlib.use("Agg")
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analyzes cleaned book dataset and generates visualizations and reports."""

    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = output_dir
        self.figures_dir = os.path.join(output_dir, "figures")
        os.makedirs(self.figures_dir, exist_ok=True)
        # Apply standard clean styling
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    def generate_summary_statistics(self) -> Dict[str, Any]:
        """Compute key data metrics and statistical aggregates."""
        df = self.df
        stats = {
            "total_books": len(df),
            "unique_categories": df["category"].nunique() if "category" in df.columns else 0,
            "price_mean": float(df["price_gbp"].mean()) if "price_gbp" in df.columns else 0.0,
            "price_median": float(df["price_gbp"].median()) if "price_gbp" in df.columns else 0.0,
            "price_std": float(df["price_gbp"].std()) if "price_gbp" in df.columns else 0.0,
            "price_min": float(df["price_gbp"].min()) if "price_gbp" in df.columns else 0.0,
            "price_max": float(df["price_gbp"].max()) if "price_gbp" in df.columns else 0.0,
            "rating_mean": float(df["star_rating"].mean()) if "star_rating" in df.columns else 0.0,
            "total_stock_units": int(df["stock_quantity"].sum()) if "stock_quantity" in df.columns else 0,
            "in_stock_count": int(df["is_in_stock"].sum()) if "is_in_stock" in df.columns else len(df),
        }
        return stats

    def plot_price_distribution(self) -> str:
        """Plot histogram of book prices with mean and median markers."""
        fig, ax = plt.subplots(figsize=(9, 5))
        prices = self.df["price_gbp"].dropna()

        ax.hist(prices, bins=25, color="#3498db", edgecolor="#2980b9", alpha=0.75, density=False)
        mean_val = prices.mean()
        median_val = prices.median()

        ax.axvline(mean_val, color="#e74c3c", linestyle="--", linewidth=2, label=f"Mean: £{mean_val:.2f}")
        ax.axvline(median_val, color="#2ecc71", linestyle="-.", linewidth=2, label=f"Median: £{median_val:.2f}")

        ax.set_title("Distribution of Book Prices (£ GBP)", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Price (£)", fontsize=11)
        ax.set_ylabel("Number of Books", fontsize=11)
        ax.legend(frameon=True, facecolor="white", framealpha=0.9)
        plt.tight_layout()

        out_path = os.path.join(self.figures_dir, "price_distribution.png")
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        logger.info(f"Saved: {out_path}")
        return out_path

    def plot_rating_distribution(self) -> str:
        """Plot frequency bar chart for star ratings."""
        fig, ax = plt.subplots(figsize=(8, 5))
        rating_counts = self.df["star_rating"].value_counts().sort_index()

        # Ensure all 1 to 5 ratings exist
        for r in range(1, 6):
            if r not in rating_counts:
                rating_counts[r] = 0
        rating_counts = rating_counts.sort_index()

        bars = ax.bar(
            [f"{r} Star{'s' if r > 1 else ''}" for r in rating_counts.index],
            rating_counts.values,
            color="#f39c12",
            edgecolor="#d68910",
            width=0.55
        )

        total = len(self.df)
        for bar in bars:
            height = bar.get_height()
            pct = (height / total) * 100 if total > 0 else 0
            ax.annotate(
                f"{height} ({pct:.1f}%)",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

        ax.set_title("Customer Star Rating Distribution", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Rating", fontsize=11)
        ax.set_ylabel("Book Count", fontsize=11)
        ax.set_ylim(0, max(rating_counts.values) * 1.15 if max(rating_counts.values) > 0 else 10)
        plt.tight_layout()

        out_path = os.path.join(self.figures_dir, "rating_distribution.png")
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        logger.info(f"Saved: {out_path}")
        return out_path

    def plot_top_categories(self, top_n: int = 10) -> str:
        """Plot top N book categories by volume."""
        fig, ax = plt.subplots(figsize=(10, 6))
        cat_counts = self.df["category"].value_counts().head(top_n).sort_values(ascending=True)

        bars = ax.barh(cat_counts.index, cat_counts.values, color="#1abc9c", edgecolor="#16a085")
        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f" {int(width)}",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(3, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold"
            )

        ax.set_title(f"Top {top_n} Book Categories by Count", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Number of Books", fontsize=11)
        ax.set_xlim(0, max(cat_counts.values) * 1.15 if len(cat_counts) > 0 else 10)
        plt.tight_layout()

        out_path = os.path.join(self.figures_dir, "top_categories.png")
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        logger.info(f"Saved: {out_path}")
        return out_path

    def plot_price_by_rating(self) -> str:
        """Plot boxplot of book price variations grouped by star rating."""
        fig, ax = plt.subplots(figsize=(8, 5))
        data_to_plot = []
        labels = []
        for r in range(1, 6):
            subset = self.df[self.df["star_rating"] == r]["price_gbp"].dropna()
            data_to_plot.append(subset)
            labels.append(f"{r} Star")

        ax.boxplot(data_to_plot, tick_labels=labels, patch_artist=True,
                   boxprops=dict(facecolor="#9b59b6", color="#8e44ad", alpha=0.7),
                   medianprops=dict(color="#2c3e50", linewidth=2),
                   whiskerprops=dict(color="#8e44ad"),
                   capprops=dict(color="#8e44ad"))

        ax.set_title("Price Distribution Across Star Ratings", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Rating", fontsize=11)
        ax.set_ylabel("Price (£ GBP)", fontsize=11)
        plt.tight_layout()

        out_path = os.path.join(self.figures_dir, "price_by_rating.png")
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        logger.info(f"Saved: {out_path}")
        return out_path

    def plot_category_avg_price(self, top_n: int = 10) -> str:
        """Plot top N categories with highest average price (min 2 books)."""
        cat_stats = self.df.groupby("category").agg(
            avg_price=("price_gbp", "mean"),
            count=("price_gbp", "count")
        )
        filtered = cat_stats[cat_stats["count"] >= 2].sort_values(by="avg_price", ascending=False).head(top_n)
        filtered = filtered.sort_values(by="avg_price", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(filtered.index, filtered["avg_price"], color="#e67e22", edgecolor="#d35400")
        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f" £{width:.2f}",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(3, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=9,
                fontweight="bold"
            )

        ax.set_title(f"Top {top_n} Highest Average Priced Categories (Min 2 Books)", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Average Price (£ GBP)", fontsize=11)
        ax.set_xlim(0, max(filtered["avg_price"]) * 1.15 if len(filtered) > 0 else 10)
        plt.tight_layout()

        out_path = os.path.join(self.figures_dir, "category_avg_price.png")
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        logger.info(f"Saved: {out_path}")
        return out_path

    def generate_report(self) -> str:
        """Write detailed summary report to text file."""
        stats = self.generate_summary_statistics()
        top_cats = self.df["category"].value_counts().head(5)
        rating_dist = self.df["star_rating"].value_counts().sort_index()

        report_lines = [
            "=" * 70,
            "      CODEALPHA DATA ANALYTICS INTERNSHIP - TASK 1: WEB SCRAPING",
            "                  DATASET ANALYSIS & AUDIT REPORT",
            "=" * 70,
            "",
            "1. EXECUTIVE SUMMARY",
            "-" * 70,
            f"Target Source:             Books to Scrape (https://books.toscrape.com)",
            f"Total Books Scraped:       {stats['total_books']}",
            f"Unique Categories:         {stats['unique_categories']}",
            f"Total Inventory Units:     {stats['total_stock_units']:,} items",
            f"Books Currently In Stock:  {stats['in_stock_count']} / {stats['total_books']}",
            "",
            "2. PRICING METRICS (GBP £)",
            "-" * 70,
            f"Average Price (Mean):      £{stats['price_mean']:.2f}",
            f"Median Price:              £{stats['price_median']:.2f}",
            f"Standard Deviation:        £{stats['price_std']:.2f}",
            f"Lowest Book Price:         £{stats['price_min']:.2f}",
            f"Highest Book Price:        £{stats['price_max']:.2f}",
            "",
            "3. STAR RATING DISTRIBUTION",
            "-" * 70,
            f"Average Star Rating:       {stats['rating_mean']:.2f} / 5.0",
        ]

        for r in range(1, 6):
            cnt = rating_dist.get(r, 0)
            pct = (cnt / stats['total_books']) * 100 if stats['total_books'] > 0 else 0
            bar = "★" * r + "☆" * (5 - r)
            report_lines.append(f"  {r} Star [{bar}]: {cnt:4d} books ({pct:5.1f}%)")

        report_lines.extend([
            "",
            "4. TOP 5 CATEGORIES BY VOLUME",
            "-" * 70,
        ])
        for cat, cnt in top_cats.items():
            report_lines.append(f"  - {cat:25s}: {cnt:3d} books")

        report_lines.extend([
            "",
            "5. DATA PIPELINE ARTIFACTS",
            "-" * 70,
            "  * Raw Data Export:         data/raw/books_raw.csv",
            "  * Cleaned CSV Export:      data/processed/books_cleaned.csv",
            "  * Cleaned JSON Export:     data/processed/books_cleaned.json",
            "  * Visualizations:          output/figures/*.png",
            "=" * 70,
        ])

        report_content = "\n".join(report_lines)
        report_path = os.path.join(self.output_dir, "scraping_summary_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        logger.info(f"Saved summary report to: {report_path}")
        return report_path

    def run_all(self) -> None:
        """Run all analytics computations and generate all visual figures."""
        logger.info("Generating exploratory data visualizations...")
        self.plot_price_distribution()
        self.plot_rating_distribution()
        self.plot_top_categories(10)
        self.plot_price_by_rating()
        self.plot_category_avg_price(10)
        self.generate_report()
        logger.info("All analytical charts and summary reports generated successfully.")
