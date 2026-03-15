#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(
        description="Count NYC 311 complaint types."
    )
    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", help="Optional output CSV file")
    return parser.parse_args()

def within_range(date_str, start, end):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return start <= date <= end
    except Exception:
        return False

def main():
    args = parse_args()
    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")

    counts = defaultdict(int)

    with open(args.input, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            created_date = row.get("created_date", "").split(" ")[0]
            if within_range(created_date, start_date, end_date):
                complaint = row.get("complaint_type", "UNKNOWN")
                borough = row.get("borough", "UNKNOWN")
                counts[(complaint, borough)] += 1

    output_lines = ["complaint type,borough,count"]
    for (complaint, borough), count in sorted(counts.items()):
        output_lines.append(f"{complaint},{borough},{count}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
    else:
        print("\n".join(output_lines))

if __name__ == "__main__":
    main()
