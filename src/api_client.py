"""REST API client for Frankfurter (European Central Bank Forex data)."""
import json
import os
import requests
from typing import Dict, Any, List

class ForexAPIClient:
    BASE_URL = "https://api.frankfurter.dev/v1"

    def __init__(self, raw_data_dir: str = "data/raw"):
        self.raw_data_dir = raw_data_dir
        os.makedirs(self.raw_data_dir, exist_ok=True)

    def fetch_historical_rates(
        self,
        start_date: str = "2024-01-01",
        end_date: str = "2024-12-31",
        base: str = "EUR",
        symbols: List[str] = None
    ) -> Dict[str, Any]:
        """Fetch historical exchange rates between dates and cache raw JSON."""
        if symbols is None:
            symbols = ["USD", "GBP", "JPY", "CAD", "CHF"]

        symbols_param = ",".join(symbols)
        endpoint = f"{self.BASE_URL}/{start_date}..{end_date}?base={base}&symbols={symbols_param}"
        
        print(f"[API] Requesting endpoint: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=15)
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.RequestException as exc:
            raise ConnectionError(f"Failed to fetch Forex data from Frankfurter API: {exc}")

        # Cache raw payload
        cache_path = os.path.join(self.raw_data_dir, f"raw_forex_{base}_{start_date}_{end_date}.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"[API] Raw payload successfully cached to {cache_path}")

        return payload