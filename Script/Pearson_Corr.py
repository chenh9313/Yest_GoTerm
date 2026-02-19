import sys
import math

def pearson_corr(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))

    return num / (den_x * den_y)


# Get filename from command line
if len(sys.argv) < 2:
    print("Usage: python test.py inputfile.txt")
    sys.exit(1)

input_file = sys.argv[1] + ".txt"
#output_file = input_file + "_pearson_corr.txt"
output_file = sys.argv[1] + "_pearson_corr.txt"

genes = []
data = []

with open(input_file, "r") as f:
    next(f)  # skip header

    for line in f:
        parts = line.strip().split("\t")
        gene = parts[0]
        values = list(map(float, parts[2:]))  # skip GeneName and Class
        genes.append(gene)
        data.append(values)


with open(output_file, "w") as out:
    out.write("Gene1\tGene2\tpearson_corr_Value\n")

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            corr = pearson_corr(data[i], data[j])
            out.write(f"{genes[i]}\t{genes[j]}\t{corr}\n")

print(f"Done! Output saved to {output_file}")
