import argparse
import json
import random
import sys

def load_reddit_posts(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        name = post.get("name", "").strip()
        title = post.get("title", "").replace("\n", " ").strip()
        if name and title:
            posts.append((name, title))
    return posts

def write_tsv(out_file, posts):
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("Name\ttitle\tcoding\n")
        for name, title in posts:
            f.write(f"{name}\t{title}\t\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_file", required=True)
    parser.add_argument("json_file")
    parser.add_argument("num_posts", type=int)
    args = parser.parse_args()

    posts = load_reddit_posts(args.json_file)

    if not posts:
        print("No posts found in file.")
        sys.exit(1)

    if args.num_posts >= len(posts):
        selected = posts
    else:
        selected = random.sample(posts, args.num_posts)

    write_tsv(args.out_file, selected)
    print(f"Wrote {len(selected)} posts to {args.out_file}")

if __name__ == "__main__":
    main()
