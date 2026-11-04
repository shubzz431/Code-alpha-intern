"""
Data Cleaning and Transformation Module
Processes raw scraped book data into structured, typed, and validated datasets.
"""

import re
import os
import logging
from typing import Union, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class DataCleaner:
    """Cleans, formats, and validates scraped book data."""

    RATING_MAP = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    @staticmethod
    def _clean_currency(val: Any) -> float:
        """Strip currency symbols, artifact encodings, and convert to float."""
        if pd.isna(val) or val is None:
            return np.nan
        val_str = str(val)
        # Extract numeric portion including decimal
        match = re.search(r"(\d+\.?\d*)", val_str)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return np.nan
        return np.nan

    @staticmethod
    def _extract_stock_quantity(val: Any) -> int:
        """Extract stock count from strings like 'In stock (22 available)'."""
        if pd.isna(val) or val is None:
            return 0
        match = re.search(r"\((\d+)\s+available\)", str(val), re.IGNORECASE)
        if match:
            return int(match.group(1))
        if "in stock" in str(val).lower():
            return 1
        return 0

    @classmethod
    def clean_dataframe(cls, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Process raw dataframe into clean schema."""
        if raw_df.empty:
            logger.warning("Empty dataframe provided to clean_dataframe.")
            return raw_df

        df = raw_df.copy()

        # 1. Clean Title
        if "title" in df.columns:
            df["title"] = df["title"].astype(str).str.strip()

        # 2. Clean Prices
        if "price_str" in df.columns:
            df["price_gbp"] = df["price_str"].apply(cls._clean_currency)
        else:
            df["price_gbp"] = np.nan

        if "price_excl_tax_str" in df.columns:
            df["price_excl_tax_gbp"] = df["price_excl_tax_str"].apply(cls._clean_currency)
        else:
            df["price_excl_tax_gbp"] = df["price_gbp"]

        if "price_incl_tax_str" in df.columns:
            df["price_incl_tax_gbp"] = df["price_incl_tax_str"].apply(cls._clean_currency)
        else:
            df["price_incl_tax_gbp"] = df["price_gbp"]

        if "tax_str" in df.columns:
            df["tax_gbp"] = df["tax_str"].apply(cls._clean_currency).fillna(0.0)
        else:
            df["tax_gbp"] = 0.0

        # Fallback for primary price
        df["price_gbp"] = df["price_gbp"].fillna(df["price_incl_tax_gbp"])

        # 3. Clean Star Rating (1 - 5)
        if "rating_str" in df.columns:
            df["star_rating"] = (
                df["rating_str"]
                .astype(str)
                .str.lower()
                .map(cls.RATING_MAP)
                .fillna(0)
                .astype(int)
            )
        else:
            df["star_rating"] = 0

        # 4. Clean Availability and Stock Quantity
        avail_col = "detail_availability" if "detail_availability" in df.columns else "availability_str"
        if avail_col in df.columns:
            df["stock_quantity"] = df[avail_col].apply(cls._extract_stock_quantity)
            df["is_in_stock"] = df["stock_quantity"] > 0
        else:
            df["stock_quantity"] = 0
            df["is_in_stock"] = False

        # 5. Clean Category
        if "category" in df.columns:
            df["category"] = df["category"].fillna("General").astype(str).str.strip()
        else:
            df["category"] = "General"

        # 6. Clean UPC & Identifier
        if "upc" in df.columns:
            df["upc"] = df["upc"].fillna("").astype(str).str.strip()
        else:
            df["upc"] = ""

        # 7. Reviews Count
        if "reviews_count" in df.columns:
            df["reviews_count"] = (
                pd.to_numeric(df["reviews_count"], errors="coerce")
                .fillna(0)
                .astype(int)
            )
        else:
            df["reviews_count"] = 0

        # 8. Description
        if "description" in df.columns:
            df["description"] = (
                df["description"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )
        else:
            df["description"] = ""

        # 9. Deduplication
        initial_len = len(df)
        if "upc" in df.columns and (df["upc"] != "").any():
            # If UPC exists, deduplicate on non-empty UPCs
            df = df.drop_duplicates(subset=["upc"], keep="first")
        else:
            df = df.drop_duplicates(subset=["title", "price_gbp"], keep="first")

        dropped = initial_len - len(df)
        if dropped > 0:
            logger.info(f"Removed {dropped} duplicate records.")

        # 10. Reorder columns
        desired_order = [
            "upc",
            "title",
            "category",
            "price_gbp",
            "price_excl_tax_gbp",
            "price_incl_tax_gbp",
            "tax_gbp",
            "star_rating",
            "is_in_stock",
            "stock_quantity",
            "reviews_count",
            "description",
            "product_url",
            "image_url",
            "page_number",
        ]
        available_order = [c for c in desired_order if c in df.columns]
        extra_cols = [c for c in df.columns if c not in desired_order and not c.endswith("_str")]
        
        final_df = df[available_order + extra_cols].reset_index(drop=True)
        logger.info(f"Cleaned dataset: {len(final_df)} records, {len(final_df.columns)} columns.")
        return final_df

    @classmethod
    def save_datasets(
        cls,
        raw_df: pd.DataFrame,
        cleaned_df: pd.DataFrame,
        raw_path: str,
        processed_csv_path: str,
        processed_json_path: str,
    ) -> None:
        """Save raw and cleaned datasets to specified paths."""
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(processed_json_path), exist_ok=True)

        raw_df.to_csv(raw_path, index=False, encoding="utf-8")
        logger.info(f"Raw dataset saved to: {raw_path}")

        cleaned_df.to_csv(processed_csv_path, index=False, encoding="utf-8")
        logger.info(f"Cleaned CSV saved to: {processed_csv_path}")

        cleaned_df.to_json(
            processed_json_path,
            orient="records",
            indent=2,
            force_ascii=False
        )
        logger.info(f"Cleaned JSON saved to: {processed_json_path}")
