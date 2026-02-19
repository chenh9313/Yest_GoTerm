#!/usr/bin/env python3

import sys
import os
import pandas as pd


def get_summary(filename):
    if not os.path.exists(filename):
        return None

    df = pd.read_csv(filename, sep="\t")

    if "pearson_corr_Value" not in df.columns:
        return None

    summary = df["pearson_corr_Value"].describe(
        percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]
    ).drop("count")

    return summary


def main():
    if len(sys.argv) != 2:
        print("Usage: python summary.py <prefix>")
        sys.exit(1)

    prefix = sys.argv[1]

    files = {
        "AllGenes": prefix + "_pearson_corr.txt",
        "Class0_vs_Class1": prefix + "_pearson_corr_Class0_vs_Class1.txt",
        "Class0_vs_Class0": prefix + "_pearson_corr_Class0_vs_Class0.txt",
        "Class1_vs_Class1": prefix + "_pearson_corr_Class1_vs_Class1.txt"
    }

    results = {}

    for label, filename in files.items():
        summary = get_summary(filename)
        if summary is not None:
            for stat_name, value in summary.items():
                clean_stat = stat_name.replace("%", "pct")
                col_name = f"{label}_{clean_stat}"
                results[col_name] = value

    if not results:
        print("No valid files found.")
        sys.exit(1)

    # Compute median difference if both medians exist
    col1 = "Class1_vs_Class1_50pct"
    col0 = "Class0_vs_Class0_50pct"

    # We stored percent names without replacing 50%, so ensure correct naming
    if col1 in results and col0 in results:
        diff_value = results[col1] - results[col0]
        results["diff50pct_Class1_vs_Class1-Class0_vs_Class0"] = diff_value

    combined = pd.DataFrame([results])
    combined.insert(0, "Name", prefix)

    output_filename = prefix + "_Summary.txt"
    combined.to_csv(output_filename, sep="\t", index=False)

    print(f"Summary written to {output_filename}")


if __name__ == "__main__":
    main()