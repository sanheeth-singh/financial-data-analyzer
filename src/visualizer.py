"""Visualization generator using Matplotlib and Seaborn."""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, figures_dir: str = "reports/figures"):
        self.figures_dir = figures_dir
        os.makedirs(self.figures_dir, exist_ok=True)
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    def generate_all_plots(self, prices_df: pd.DataFrame, returns_df: pd.DataFrame) -> str:
        """Create a 4-panel dashboard figure and save as high-resolution PNG."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 11))
        plt.subplots_adjust(hspace=0.32, wspace=0.25)

        # 1. Price trajectory with 30-day SMA for USD
        primary_curr = "USD" if "USD" in prices_df.columns else prices_df.columns[0]
        sma30 = prices_df[primary_curr].rolling(window=30).mean()
        axes[0, 0].plot(prices_df.index, prices_df[primary_curr], label=f"Spot Rate ({primary_curr})", color="#1f77b4", lw=1.5)
        axes[0, 0].plot(prices_df.index, sma30, label="30-Day Moving Avg", color="#ff7f0e", linestyle="--")
        axes[0, 0].set_title(f"Exchange Rate Trend & 30D SMA ({primary_curr})", fontsize=11, fontweight="bold")
        axes[0, 0].set_ylabel("Exchange Rate")
        axes[0, 0].legend()

        # 2. Return distributions (Hist + KDE)
        comp_curr = [c for c in ["USD", "GBP"] if c in returns_df.columns]
        for c in comp_curr:
            sns.histplot(returns_df[c], kde=True, ax=axes[0, 1], label=f"{c} Daily Return", bins=30, stat="density", alpha=0.4)
        axes[0, 1].set_title("Return Density & Volatility Spread", fontsize=11, fontweight="bold")
        axes[0, 1].set_xlabel("Daily Return")
        axes[0, 1].legend()

        # 3. Correlation Heatmap
        corr = returns_df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=axes[1, 0], cbar=True)
        axes[1, 0].set_title("Return Correlation Matrix", fontsize=11, fontweight="bold")

        # 4. Box Plot (Spread & Outlier Detection)
        sns.boxplot(data=returns_df, palette="Set2", ax=axes[1, 1])
        axes[1, 1].set_title("Daily Return Dispersion (Box Plots)", fontsize=11, fontweight="bold")
        axes[1, 1].set_ylabel("Daily Return")

        plt.suptitle("Automated Financial Visual Analytics Dashboard", fontsize=15, fontweight="bold", y=0.95)

        output_path = os.path.join(self.figures_dir, "market_analytics_dashboard.png")
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"[Visualizer] Visual dashboard generated and saved to: {output_path}")

        return output_path