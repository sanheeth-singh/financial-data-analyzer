"""Main entry point for Financial Data Analysis Application."""
import argparse
from src.api_client import ForexAPIClient
from src.cleaner import DataCleaner
from src.analyzer import FinancialAnalyzer
from src.visualizer import Visualizer
from src.report_gen import ReportGenerator

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automated Forex Data Ingestion, Analysis, and Report Pipeline")
    parser.add_argument("--start", type=str, default="2025-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2025-12-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--base", type=str, default="EUR", help="Base currency code (e.g., EUR, USD)")
    parser.add_argument("--symbols", nargs="+", default=["USD", "GBP", "JPY", "CAD", "CHF"], help="Quote currency symbols")
    return parser.parse_args()

def main():
    args = parse_arguments()
    print("=" * 67)
    print("bunnyMe9 FINANCIAL DATA & API ANALYSIS PIPELINE")
    print(f"Parameters: {args.base} vs {args.symbols} ({args.start} to {args.end})")
    print("=" * 67)

    # 1. Ingestion via REST API
    client = ForexAPIClient()
    payload = client.fetch_historical_rates(
        start_date=args.start,
        end_date=args.end,
        base=args.base,
        symbols=args.symbols
    )

    # 2. Cleaning & Processing
    cleaner = DataCleaner()
    prices_df = cleaner.process_rates_payload(payload)

    # 3. Financial Analysis
    analyzer = FinancialAnalyzer(prices_df)
    summary_stats = analyzer.compute_summary_statistics()
    corr_matrix = analyzer.compute_correlation_matrix()
    executive_metrics = analyzer.extract_executive_metrics()

    # 4. Data Visualization
    visualizer = Visualizer()
    visualizer.generate_all_plots(prices_df, analyzer.returns_df)

    # 5. Report Generation
    report_gen = ReportGenerator()
    report_gen.build_report(
        metrics=executive_metrics,
        summary_df=summary_stats,
        corr_df=corr_matrix
    )

    print("=" * 67)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("Processed CSV:   data/processed/")
    print("Charts:          reports/figures/market_analytics_dashboard.png")
    print("Markdown Report: reports/financial_report.md")
    print("=" * 67)

if __name__ == "__main__":
    main()