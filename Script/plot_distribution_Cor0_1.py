#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np

def read_values(filename):
    """Read third column (pearson_corr_Value) as float list."""
    values = []
    with open(filename, 'r') as f:
        next(f)  # skip header
        for line in f:
            cols = line.strip().split("\t")
            if len(cols) >= 3:
                try:
                    values.append(float(cols[2]))
                except ValueError:
                    continue
    return values

def main():
    if len(sys.argv) != 2:
        print("Usage: python plot_4_distributions.py <prefix>")
        sys.exit(1)

    prefix = sys.argv[1]

    # Custom order of files
    filenames = [
        prefix + "_pearson_corr.txt",
        prefix + "_pearson_corr_Class0_vs_Class1.txt",
        prefix + "_pearson_corr_Class0_vs_Class0.txt",
        prefix + "_pearson_corr_Class1_vs_Class1.txt"
    ]

    # Short labels for subplot titles in the same order
    short_titles = [
        "All Genes",
        "Class0_vs_Class1",
        "Class0_vs_Class0",
        "Class1_vs_Class1"
    ]

    # Histogram color (same for all)
    hist_color = 'skyblue'

    # Read values for all files
    all_values = []
    for fname in filenames:
        values = read_values(fname)
        all_values.append(values)
        print(f"{fname}: {len(values)} values read")

    # Create 20 bins from 0 to 1
    bin_edges = np.linspace(0, 1, 21)

    # Calculate max frequency for unified y-axis
    max_count = 0
    for values in all_values:
        counts, _ = np.histogram(values, bins=bin_edges)
        max_count = max(max_count, counts.max())

    # Plot 4 histograms on a single figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, values in enumerate(all_values):
        axes[i].hist(values, bins=bin_edges, color=hist_color, edgecolor='black')
        axes[i].set_title(short_titles[i], fontsize=12)
        axes[i].set_xlabel("Pearson Correlation")
        axes[i].set_ylabel("Frequency")
        axes[i].grid(axis='y', alpha=0.7)
        axes[i].set_ylim(0, max_count + 1)  # unified y-axis
        axes[i].set_xlim(0, 1)  # x-axis always 0-1

        # Add median line
        median_val = np.median(values)
        axes[i].axvline(median_val, color='red', linestyle='dashed', linewidth=1.5)

        # Place median text horizontally above the line
        top_y = max_count * 0.95
        axes[i].text(median_val - 0.02, top_y, f'Median={median_val:.2f}',
                     horizontalalignment='right', verticalalignment='bottom',
                     color='black', fontsize=10)

    plt.tight_layout()

    # Save as PDF
    pdf_filename = prefix + "_pearson_corr_distributions.pdf"
    plt.savefig(pdf_filename)
    print(f"\nAll distributions saved in: {pdf_filename}")

    # Optional: show plot
    # plt.show()

if __name__ == "__main__":
    main()

