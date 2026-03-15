import csv
from collections import Counter, OrderedDict

import matplotlib.pyplot as plt


MCGILL_FILE = "final_labeled_dataset_mcgill.tsv"
CONCORDIA_FILE = "final_labeled_dataset_concordia.tsv"
OUTPUT_FIG = "results.png"

CODE_MAP = OrderedDict([
    ("a", "Exams & Courses"),
    ("b", "Academic Admin / Degree Progress"),
    ("c", "Campus Facilities & Services"),
    ("d", "Social Activities & Clubs"),
    ("e", "Jobs & Opportunities"),
    ("f", "Health, Immigration & Well-Being"),
    ("g", "Governance & Student Politics"),
    ("h", "General Discussion / Rants / Misc"),
])



def load_counts(tsv_path):
    """
    Load a TSV file and return a Counter of category frequencies.
    Assumes there is a 'coding' column whose values look like:
       'a) Exams & Courses'  OR  'a) ...'  OR  'a)'
    """
    counts = Counter()
    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            raw = row.get("coding", "")
            if not raw:
                continue
            raw = raw.strip().lower()
            code_letter = raw[0]  # 'a', 'b', etc.
            if code_letter in CODE_MAP:
                category = CODE_MAP[code_letter]
                counts[category] += 1
    return counts


def counts_to_relative(counts):
    total = sum(counts.values())
    if total == 0:
        return {k: 0.0 for k in CODE_MAP.values()}
    return {k: counts.get(k, 0) / total for k in CODE_MAP.values()}


def main():
    mcgill_counts = load_counts(MCGILL_FILE)
    concordia_counts = load_counts(CONCORDIA_FILE)

    mcgill_rel = counts_to_relative(mcgill_counts)
    concordia_rel = counts_to_relative(concordia_counts)

    categories = list(CODE_MAP.values())
    x = range(len(categories))

    mcgill_vals = [mcgill_rel[c] for c in categories]
    concordia_vals = [concordia_rel[c] for c in categories]

    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in x], mcgill_vals, width, label="McGill")
    plt.bar([i + width/2 for i in x], concordia_vals, width, label="Concordia")

    plt.xticks(x, categories, rotation=45, ha="right")
    plt.ylabel("Relative abundance (proportion of posts)")
    plt.title("Topic distribution on r/mcgill vs r/concordia")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_FIG, dpi=200)

    # Also print numeric values to the terminal
    print("McGill counts:", mcgill_counts)
    print("Concordia counts:", concordia_counts)
    print(f"Saved figure to {OUTPUT_FIG}")


if __name__ == "__main__":
    main()
