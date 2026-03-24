![Tests](https://github.com/Aminesbaillo/cafe-sales-cleaner/actions/workflows/tests.yml/badge.svg)

# Cafe Sales Data Cleaner

> A lightweight, extensible Python pipeline that automatically detects, audits, and cleans dirty CSV data  and generates a human-readable report of every fix applied.

---

## The Problem

Raw sales data is rarely clean. It arrives with invalid placeholders like `ERROR` and `UNKNOWN`, missing values, inconsistent formatting, and broken numeric fields. Cleaning this manually is slow, error-prone, and not reproducible.

---

## The Solution

This pipeline automatically:
- Detects the type of each column (numeric, categorical, date, id)
- Audits each column for problems based on its type
- Cleans each column using type-specific rules
- Recalculates derived columns when possible (e.g. Total Spent = Quantity  Price)
- Exports a cleaned CSV ready for analysis
- Generates a markdown report summarizing every problem found and every fix applied

No hardcoded column names. No manual rules per dataset. Add a new CSV and it just works.

---

## How It Works

The pipeline runs in 6 steps:

**1. Load**  reads the raw CSV, standardizes column names to lowercase with underscores.

**2. Detect**  inspects each column and infers its type:
- `id`  column name contains "id"
- `date`  column name contains "date" or values parse as dates
- `numeric`  80%+ of non-null values are numbers
- `categorical`  low cardinality relative to row count
- `text`  everything else

**3. Audit**  scans each column for problems based on its detected type:
- counts nulls and invalid placeholders (ERROR, UNKNOWN)
- checks numeric columns for non-numeric values
- checks date columns for unparseable values
- lists unique valid values for categorical columns

**4. Clean**  fixes each column based on its detected type:
- replaces ERROR and UNKNOWN with NaN
- converts numeric columns to float
- parses date columns to datetime
- strips whitespace from all string columns

**5. Recalculate**  recovers derived columns when possible (configurable via main.py).

**6. Export**  saves the cleaned CSV and generates a markdown report.

---

## Quickstart
```bash
# Clone the repo
git clone https://github.com/Aminesbaillo/cafe-sales-cleaner.git
cd cafe-sales-cleaner

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python main.py
```

Or with custom paths:
```bash
python main.py --input data/raw/your_file.csv --output data/cleaned/out.csv --report reports/report.md
```

---

## Output

| File | Description |
|------|-------------|
| `data/cleaned/cleaned_cafe_sales.csv` | Fully cleaned dataset ready for analysis |
| `reports/cleaning_report.md` | Human-readable report of all problems found and fixes applied |

---

## How To Expand It

The pipeline is designed to be extended without touching existing logic:

| Goal | What to change |
|------|---------------|
| Support a new column type | Add detection in `detector.py`, audit logic in `auditor.py`, cleaning logic in `cleaner.py` |
| Support a new invalid placeholder | Add it to `INVALID_PLACEHOLDERS` in `detector.py` and `cleaner.py` |
| Add a new derived column rule | Add an entry to `derived_columns` in `main.py` |
| Clean a different CSV | Pass `--input your_file.csv`  no code changes needed |
| Add more date formats | Add the format string to `COMMON_DATE_FORMATS` in `detector.py` |

---

## Tech Stack

- Python 3.12
- pandas
- numpy
- pytest
- GitHub Actions

---

## Dataset

The raw dataset used is the [Dirty Cafe Sales CSV](data/raw/dirty_cafe_sales.csv)  a synthetic dataset with intentional data quality issues including missing values, invalid placeholders, and inconsistent formatting.
