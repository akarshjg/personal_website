import csv
import sys
import os

sys.path.append(os.path.abspath("scripts"))
from import_goodreads_csv import classify_book, clean_title

with open("goodreads_library_export.csv", mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    uncategorized = []
    for row in reader:
        title = row.get("Title", "").strip()
        author = row.get("Author", "").strip()
        additional_authors = row.get("Additional Authors", "").strip()
        authors = [author]
        if additional_authors:
            for aa in additional_authors.split(','):
                authors.append(aa.strip())
        
        shelves = row.get("Bookshelves", "")
        exclusive_shelf = row.get("Exclusive Shelf", "")
        
        title_clean = clean_title(title)
        cat = classify_book(title_clean, authors, shelves, exclusive_shelf)
        if cat == "My reading list":
            uncategorized.append((title_clean, authors, shelves, exclusive_shelf))

print(f"Total uncategorized: {len(uncategorized)}")
for i, (t, a, s, es) in enumerate(uncategorized, 1):
    print(f"{i}. Title: {t} | Authors: {a} | Shelves: {s} | Exclusive: {es}")
