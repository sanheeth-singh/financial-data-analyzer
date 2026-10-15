"""Data cleaning, type casting, and preprocessing module."""
import os
import pandas as pd
from typing import Dict, Any

class DataCleaner:
    def __init__(self, processed_data_dir: str = "data/processed"):
        self.processed_data_dir = processed_data_dir
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def process_rates_payload(self, payload: Dict[str, Any]) -> pd.DataFrame:
        """Convert raw rates JSON dictionary into a cleaned, validated DataFrame."""
        raw_rates = payload.get("rates", {})
        if not raw_rates:
            raise ValueError("Payload contains no rate data to process.")

        # Convert dictionary to DataFrame (dates as index)
        df = pd.DataFrame.from_dict(raw_rates, orient="index")
        
        # Datetime conversion and sorting
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"
        df = df.sort_index()

        # Handle missing market holiday dates via forward-fill then backward-fill
        initial_nulls = df.isna().sum().sum()
        if initial_nulls > 0:
            print(f"[Cleaner] Detected {initial_nulls} missing entries. Applying forward fill.")
            df = df.ffill().bfill()

        # Ensure float datatypes
        df = df.astype(float)

        # Save processed CSV
        base_curr = payload.get("base", "EUR")
        csv_filename = f"forex_{base_curr}_processed.csv"
        csv_path = os.path.join(self.processed_data_dir, csv_filename)
        df.to_csv(csv_path)
        print(f"[Cleaner] Cleaned dataset saved to: {csv_path} ({df.shape[0]} rows, {df.shape[1]} columns)")

        return df