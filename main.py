import argparse
from src.pipeline import run_pipeline

def parse_args():
    parser = argparse.ArgumentParser(
        description="Clean a dirty CSV file and generate a cleaning report."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/dirty_cafe_sales.csv",
        help="Path to the raw input CSV file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/cleaned/cleaned_cafe_sales.csv",
        help="Path to save the cleaned CSV file.",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="reports/cleaning_report.md",
        help="Path to save the cleaning report.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        input_path=args.input,
        output_csv_path=args.output,
        output_report_path=args.report,
        derived_columns=[
            {
                "target": "total_spent",
                "factors": ["quantity", "price_per_unit"]
            }
        ],
    )
