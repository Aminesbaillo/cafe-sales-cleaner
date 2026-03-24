# Cafe Sales Data Cleaner

## Project Overview
Cafe Sales Data Cleaner is a Python tool that takes a dirty cafe sales CSV, cleans it automatically, and exports a cleaned CSV plus a markdown report summarizing the data quality issues found and the fixes applied.

## Project Structure
```text
cafe-sales-cleaner/
 data/
    raw/              # Original dirty CSV
    cleaned/          # Exported cleaned CSV
 notebooks/
    explore.ipynb     # Data exploration notebook
 reports/
    cleaning_report.md
 src/
    loader.py         # Load raw CSV
    detector.py       # Infer column types
    auditor.py        # Find problems per column
    cleaner.py        # Fix problems per column
    pipeline.py       # Orchestrates all steps
    report_generator.py
 main.py
 requirements.txt
 README.md
```

## How It Works
- Load: Read the raw cafe sales CSV from the `data/raw/` directory.
- Detect: Infer column types so each field can be processed correctly.
- Audit: Identify data quality issues for each column before cleaning.
- Clean & Export: Apply cleaning rules, export the cleaned CSV, and generate the markdown report.

## Quickstart
```bash
git clone <repository-url>
cd cafe-sales-cleaner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Output
Running the pipeline produces a cleaned CSV in `data/cleaned/` and a markdown summary report at `reports/cleaning_report.md`. The report captures detected column types, audit findings, and a per-column cleaning summary.

## Tech Stack
- Python 3.11
- pandas
- numpy
