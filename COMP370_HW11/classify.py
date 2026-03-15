import csv
import time
from google import genai

INPUT_CSV = "gold.csv"
OUTPUT_CSV = "llm.csv"
MODEL_NAME = "gemini-2.5-flash"  

CATEGORIES = [
    "Exams & Courses",
    "Academic Admin / Degree Progress",
    "Campus Facilities & Services",
    "Social Activities & Clubs",
    "Jobs & Opportunities",
    "Health, Immigration & Well-Being",
    "Governance & Student Politics",
    "General Discussion",
]

client = genai.Client()


def build_prompt(title: str) -> str:
    """Prompt template for classification."""
    cat_list = "\n".join(f"- {c}" for c in CATEGORIES)
    return f"""
You are annotating Reddit titles from McGill and Concordia university subreddits.

Assign exactly ONE of the following categories to the post title.
Return ONLY the category name, copied EXACTLY from the list.

Categories:
{cat_list}

Post title:
\"\"\"{title}\"\"\"
"""


def classify_title(title: str) -> str:
    prompt = build_prompt(title)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    raw = (response.text or "").strip()

    for cat in CATEGORIES:
        if cat.lower() in raw.lower():
            return cat

    return "General Discussion"


def main():
    with open(INPUT_CSV, encoding="utf-8") as fin, \
         open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as fout:

        reader = csv.DictReader(fin)
        fieldnames = ["id", "title", "llm_label"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            pid = row["id"]
            title = row["title"]

            try:
                label = classify_title(title)
            except Exception as e:
                print(f"Error on {pid}: {e}")
                label = "ERROR"

            writer.writerow({
                "id": pid,
                "title": title,
                "llm_label": label,
            })

            time.sleep(0.4)

    print(f"Wrote LLM annotations to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
