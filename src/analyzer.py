"""Financial analytics engine using NumPy and Pandas vectorized operations."""
import numpy as np
import pandas as pd
from typing import Dict, Any

class FinancialAnalyzer:
    TRADING_DAYS_PER_YEAR = 252

    def __init__(self, prices_df: pd.DataFrame):
        self.prices_df = prices_df
        # Daily percentage change
        self.returns_df = prices_df.pct_change().dropna()

    def compute_log_returns(self) -> pd.DataFrame:
        """Vectorized log returns using numpy: ln(P_t / P_{t-1})."""
        raw_values = self.prices_df.values
        log_ret = np.log(raw_values[1:] / raw_values[:-1])
        return pd.DataFrame(log_ret, index=self.prices_df.index[1:], columns=self.prices_df.columns)

    def compute_summary_statistics(self) -> pd.DataFrame:
        """Generate high-level financial risk/return performance metrics."""
        ann_vol = self.returns_df.std() * np.sqrt(self.TRADING_DAYS_PER_YEAR) * 100
        total_ret = ((self.prices_df.iloc[-1] - self.prices_df.iloc[0]) / self.prices_df.iloc[0]) * 100
        daily_mean = self.returns_df.mean() * 100

        summary = pd.DataFrame({
            "Initial Rate": self.prices_df.iloc[0].round(4),
            "Final Rate": self.prices_df.iloc[-1].round(4),
            "Total Return (%)": total_ret.round(2),
            "Daily Mean Return (%)": daily_mean.round(4),
            "Annualized Volatility (%)": ann_vol.round(2),
            "Max Spot": self.prices_df.max().round(4),
            "Min Spot": self.prices_df.min().round(4)
        })
        return summary

    def compute_correlation_matrix(self) -> pd.DataFrame:
        """Pairwise daily return correlation matrix."""
        return self.returns_df.corr().round(3)

    def extract_executive_metrics(self) -> Dict[str, Any]:
        """Extract key highlight points for report generation."""
        summary = self.compute_summary_statistics()
        most_volatile = summary["Annualized Volatility (%)"].idxmax()
        best_performer = summary["Total Return (%)"].idxmax()
        worst_performer = summary["Total Return (%)"].idxmin()

        return {
            "trading_days": len(self.prices_df),
            "start_date": self.prices_df.index[0].strftime("%Y-%m-%d"),
            "end_date": self.prices_df.index[-1].strftime("%Y-%m-%d"),
            "currencies_tracked": list(self.prices_df.columns),
            "most_volatile": most_volatile,
            "max_volatility": summary.loc[most_volatile, "Annualized Volatility (%)"],
            "best_performer": best_performer,
            "best_return": summary.loc[best_performer, "Total Return (%)"],
            "worst_performer": worst_performer,
            "worst_return": summary.loc[worst_performer, "Total Return (%)"],
        }