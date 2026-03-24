from src.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(
        input_path="data/raw/dirty_cafe_sales.csv",
        output_csv_path="data/cleaned/cleaned_cafe_sales.csv",
        output_report_path="reports/cleaning_report.md",
        derived_columns=[
            {
                "target": "total_spent",
                "factors": ["quantity", "price_per_unit"]
            }
        ],
    )
