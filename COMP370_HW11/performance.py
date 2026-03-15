import csv

GOLD_FILE = "gold.csv"
LLM_FILE = "llm.csv"
CONFUSION_OUT = "confusion.csv"
PR_OUT = "precision_recall.csv"


def load_labels(path, label_field):
    """Return dict: id -> label."""
    mapping = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row["id"]] = row[label_field].strip()
    return mapping


def main():
    gold = load_labels(GOLD_FILE, "gold_label")
    llm = load_labels(LLM_FILE, "llm_label")

    labels = sorted(set(gold.values()) | set(llm.values()))

    confusion = {g: {p: 0 for p in labels} for g in labels}

    for pid, g_label in gold.items():
        p_label = llm.get(pid, "MISSING")
        if p_label not in labels:
            labels.append(p_label)
            for row in confusion.values():
                row[p_label] = 0
            confusion[p_label] = {p: 0 for p in labels}
        confusion[g_label][p_label] += 1

    with open(CONFUSION_OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([""] + labels)  
        for g in labels:
            row = [g] + [confusion[g][p] for p in labels]
            writer.writerow(row)

    with open(PR_OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "precision", "recall"])
        for L in labels:
            tp = confusion[L][L]
            fp = sum(confusion[g][L] for g in labels if g != L)
            fn = sum(confusion[L][p] for p in labels if p != L)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

            writer.writerow([L, f"{precision:.3f}", f"{recall:.3f}"])

    print(f"Wrote {CONFUSION_OUT} and {PR_OUT}")


if __name__ == "__main__":
    main()
