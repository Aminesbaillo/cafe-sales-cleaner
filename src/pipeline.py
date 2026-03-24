import logging

from src.loader import load_raw
from src.detector import detect_column_types
from src.auditor import audit_dataframe
from src.cleaner import clean_dataframe
from src.report_generator import generate_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_pipeline(
    input_path: str,
    output_csv_path: str,
    output_report_path: str,
    derived_columns: list[dict] | None = None,
) -> None:

    # Step 1: Load
    logger.info("Loading data...")
    df = load_raw(input_path)
    original_rows = len(df)
    logger.info(f"  {original_rows} rows loaded.")

    # Step 2: Detect column types
    logger.info("Detecting column types...")
    column_types = detect_column_types(df)
    for col, col_type in column_types.items():
        logger.info(f"  {col}: {col_type}")

    # Step 3: Audit
    logger.info("Auditing data...")
    audit_results = audit_dataframe(df, column_types)
    for col, problems in audit_results.items():
        for problem, value in problems.items():
            if problem == "unique_valid_values":
                continue
            if isinstance(value, int) and value > 0:
                logger.warning(f"  [{col}] {problem}: {value}")

    # Step 4: Clean
    logger.info("Cleaning data...")
    cleaned_df, fix_stats = clean_dataframe(df, column_types, derived_columns=derived_columns)
    cleaned_rows = len(cleaned_df)
    logger.info(f"  {cleaned_rows} rows after cleaning.")
    for col, stats in fix_stats.items():
        null_diff = stats["null_after"] - stats["null_before"]
        if null_diff > 0:
            logger.info(f"  [{col}] nulls introduced by cleaning: {null_diff}")
        elif null_diff < 0:
            logger.info(f"  [{col}] nulls recovered by recalculation: {abs(null_diff)}")

    # Step 5: Export cleaned CSV
    logger.info("Exporting cleaned CSV...")
    cleaned_df.to_csv(output_csv_path, index=False)
    logger.info(f"  Saved to {output_csv_path}")

    # Step 6: Generate report
    logger.info("Generating report...")
    generate_report(
        column_types=column_types,
        audit_results=audit_results,
        fix_stats=fix_stats,
        original_rows=original_rows,
        cleaned_rows=cleaned_rows,
        output_path=output_report_path,
    )

    logger.info("Pipeline complete.")
