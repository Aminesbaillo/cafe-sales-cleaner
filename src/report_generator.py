from datetime import datetime


def generate_report(
    column_types: dict,
    audit_results: dict,
    fix_stats: dict,
    original_rows: int,
    cleaned_rows: int,
    output_path: str,
) -> None:
    """Write a human-readable cleaning report to a markdown file."""

    lines = []
    lines.append("# Data Cleaning Report")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"\n**Original rows:** {original_rows}")
    lines.append(f"**Cleaned rows:** {cleaned_rows}")
    lines.append(f"**Duplicates removed:** {original_rows - cleaned_rows}")

    lines.append("\n---\n")
    lines.append("## Detected Column Types\n")
    for col, col_type in column_types.items():
        lines.append(f"- `{col}`: {col_type}")

    lines.append("\n---\n")
    lines.append("## Audit Results (before cleaning)\n")
    for col, problems in audit_results.items():
        lines.append(f"### {col}")
        for problem, value in problems.items():
            lines.append(f"- {problem}: {value}")
        lines.append("")

    lines.append("\n---\n")
    lines.append("## Cleaning Summary (per column)\n")
    for col, stats in fix_stats.items():
        null_diff = stats["null_before"] - stats["null_after"]
        lines.append(f"### {col} *(type: {stats['type']})*")
        lines.append(f"- Nulls before: {stats['null_before']}")
        lines.append(f"- Nulls after:  {stats['null_after']}")
        if null_diff < 0:
            lines.append(f"- Values converted to null (invalid placeholders + unparseable): {abs(null_diff)}")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report saved to {output_path}")
