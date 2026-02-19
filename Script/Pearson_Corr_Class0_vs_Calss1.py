#!/usr/bin/env python3

import sys

def load_pairs(filename):
    pairs = set()
    with open(filename, 'r') as f:
        next(f)  # skip header
        for line in f:
            cols = line.strip().split("\t")
            if len(cols) >= 2:
                pairs.add((cols[0], cols[1]))
    return pairs

def main():
    if len(sys.argv) != 2:
        print("Usage: python code.py <prefix>")
        sys.exit(1)

    prefix = sys.argv[1]

    # Automatically construct filenames
    file1 = prefix + "_pearson_corr.txt"
    file2 = prefix + "_pearson_corr_Class0_vs_Class0.txt"
    file3 = prefix + "_pearson_corr_Class1_vs_Class1.txt"
    output_file = prefix + "_pearson_corr_Class0_vs_Class1.txt"

    print("Reading:")
    print(file1)
    print(file2)
    print(file3)

    # Load pairs to remove
    pairs_to_remove = load_pairs(file2)
    pairs_to_remove.update(load_pairs(file3))

    # Filter file1
    with open(file1, 'r') as f1, open(output_file, 'w') as out:
        header = f1.readline()
        out.write(header)

        for line in f1:
            cols = line.strip().split("\t")
            if len(cols) >= 2:
                pair = (cols[0], cols[1])
                if pair not in pairs_to_remove:
                    out.write(line)

    print(f"\nFiltered file saved as: {output_file}")

if __name__ == "__main__":
    main()

