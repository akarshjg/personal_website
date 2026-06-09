#!/usr/bin/env python3
import csv
import os
import re
import sys

def slugify(text):
    text = text.lower()
    # Remove apostrophes
    text = text.replace("'", "").replace("’", "")
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading/trailing hyphens
    return text.strip('-')

def clean_title(title):
    return title.strip().strip('"').strip("'")

def classify_book(title, authors_list, shelves, exclusive_shelf):
    title_lower = title.lower()
    authors_lower = " ".join(authors_list).lower()
    
    # 1. Poetry
    poetry_keywords = ["poetry", "poem", "verse", "lyrics", "song", "ghazal", "soliloquies", "poems"]
    poetry_authors = ["gulzar", "tagore", "rumi", "rossetti", "keats", "wordsworth", "thayil"]
    if any(k in title_lower for k in poetry_keywords) or any(a in authors_lower for a in poetry_authors):
        return "Poetry"
        
    # 2. Philosophy
    philosophy_keywords = ["philosophy", "philosophical", "wisdom", "stoic", "ethics", "republic", "zarathustra", "meditations", "soliloquies", "art of war"]
    philosophy_authors = ["nietzsche", "plato", "aristotle", "aurelius", "seneca", "epictetus", "machiavelli", "sartre", "camus", "kierkegaard", "kant", "hegel", "descartes", "locke", "hume", "spinoza", "schopenhauer", "chanakya", "sun tzu", "wilde", "hofstadter", "emerson"]
    if any(k in title_lower for k in philosophy_keywords) or any(a in authors_lower for a in philosophy_authors):
        return "Philosophy"
        
    # 3. Fiction
    fiction_keywords = [
        "novel", "story", "stories", "fiction", "thriller", "mystery", "detective", 
        "harry potter", "mistborn", "fantasy", "sci-fi", "science fiction", "drama", 
        "plays", "tales", "caves", "hardy boys", "hardy-boys", "adventures", "chronicles", "reacher", 
        "godfather", "mockingbird", "fountainhead", "alchemist", "thieves", "chronicle",
        "whistler", "library", "patient", "love", "bookstore", "umbrella", "station", 
        "highway", "afternoon", "morisaki", "stationery", "brass", "covenant", "trees", 
        "crawdads", "mango", "trilogy", "partition", "runner", "nights", "stranger", "solitude"
    ]
    fiction_authors = [
        "sanderson", "rowling", "brown", "hemingway", "austen", "dixon", "tolkien", 
        "martin", "orwell", "huxley", "hemingway", "dostoevsky", "tolstoy", "dickens", 
        "twain", "fitzgerald", "woolf", "joyce", "kafka", "marquez", "lahiri", 
        "christie", "doyle", "archer", "child", "follett", "grisham", "king", 
        "clarke", "asimov", "le guin", "vance", "rothfuss", "hobb", "abercrombie", 
        "erikson", "jordan", "pratchett", "gaiman", "murakami", "kundera", "hessen", 
        "calvino", "eco", "borges", "nabokov", "proust", "faulkner", "steinbeck", 
        "melville", "hawthorne", "poe", "shelley", "stoker", "verne", "wells", 
        "kipling", "london", "wodehouse", "dahl", "golding", "salinger", "lee", 
        "capote", "heller", "vonnegut", "kesey", "plath", "morrison", "atwood", 
        "rushdie", "roy", "ghosh", "adiga", "bhagat", "sanghi", "patel", "tripathi", 
        "amitava kumar", "lahiri", "hosseini", "ishiguro", "bond", "saint-exupery", 
        "arudpragasam", "bradbury", "towles", "rijneveld", "bukowski", "dazai", 
        "kawaguchi", "kotone", "shinkai", "divakaruni", "yagisawa", "anno", "kamali", 
        "sonne", "stockett", "chakraborty", "zevin", "verghese", "shafak", "umrigar", 
        "williams", "reilly", "shanbhag", "henn", "backman", "schwarzenbach", "desai", 
        "de rosnay", "krishnamurthy", "karunatilaka", "diaz", "dubey", "paramaditha", 
        "ransmayr", "unnikrishnan", "chambers", "robinson", "serle", "rooney", "penner", 
        "owens", "nagamatsu", "mandel", "ng", "cisneros", "achebe", "pasternak", "hesse", 
        "parton", "patterson", "stuart", "mitchell", "hanif", "mundra", "sheldon", 
        "bagshawe", "riordan", "shiva", "clifton", "someshwar"
    ]
    if any(k in title_lower for k in fiction_keywords) or any(a in authors_lower for a in fiction_authors):
        return "Fiction"
        
    # 4. Non-Fiction
    nonfiction_keywords = [
        "non-fiction", "nonfiction", "biography", "memoir", "autobiography", "history", 
        "economics", "economy", "business", "marketing", "management", "strategy", 
        "design", "devops", "software", "agile", "science", "math", "physics", 
        "chemistry", "body", "genetics", "internet", "digital", "technology", 
        "startup", "investing", "finance", "data", "analysis", "psychology", 
        "mind", "brain", "habits", "success", "guide", "how to", "teach you", 
        "learn", "study", "report", "brief history", "blood", "kashmir", "economics",
        "thinking", "billion", "we indians", "himalayas", "drowning", "bed", 
        "advertising", "happiest", "creativity", "pianos", "bookshelf", "yearbook", 
        "negotiating", "negotiate", "negotiations", "netflix", "reinvention", 
        "dopamine", "poverty", "rescue", "animals", "sorrow", "longing"
    ]
    nonfiction_authors = [
        "godin", "kalanithi", "gopakumar", "ria chopra", "drucker", "porter", "collins", 
        "sinek", "ries", "covey", "clear", "duhigg", "kahneman", "tversky", "thaler", 
        "shiller", "piketty", "harari", "dawkins", "tyson", "hawking", "feynman", 
        "sagan", "pinker", "gladwell", "leavitt", "dubner", "fergiss", "isaacson", 
        "chernow", "mccullough", "goodwin", "ambedkar", "nehru", "gandhi", "kalam", 
        "sen", "panagariya", "rajan", "nilekani", "subbarao", "guha", "thapar", 
        "dalrymple", "ferguson", "diamond", "westover", "obama", "clinton", "bush", 
        "jobs", "gates", "musk", "buffett", "bogle", "malkiel", "graham", "fisher", 
        "lynch", "dalio", "schwab", "carnegie", "pease", "robbins", "ferriss", "holiday", 
        "manson", "feynman", "coleman", "lineen", "kanisetti", "albom", "macfarquhar", 
        "wang", "mcraven", "stolzoff", "choudhry", "jani", "gottlieb", "perkins", 
        "ogilvy", "jaku", "wade", "sautoy", "halifax", "walker", "gertner", "roberts", 
        "perur", "khan", "pyne", "tejubehan", "klein", "kay", "haig", "frankl", 
        "zauner", "zaleski", "cain", "angelou", "rosling", "labatut", "freud", 
        "zhuo", "mccord", "perkins", "henry", "singer", "perry", "sullivan", 
        "voss", "hastings", "singer", "emerson", "keller", "lembke", "mcdowell", 
        "pandey", "godse", "gryta", "park", "rastogi", "garcia", "miralles", 
        "taylor", "camp", "hofstadter", "deshmukh", "mathew", "kiyosaki", "agarwal", 
        "bansal"
    ]
    if any(k in title_lower for k in nonfiction_keywords) or any(a in authors_lower for a in nonfiction_authors):
        return "Non-Fiction"

    # Fallback to shelves text mapping
    shelves_lower = (shelves + " " + exclusive_shelf).lower()
    if "poetry" in shelves_lower:
        return "Poetry"
    elif "philosophy" in shelves_lower:
        return "Philosophy"
    elif "fiction" in shelves_lower:
        return "Fiction"
    elif "non-fiction" in shelves_lower or "nonfiction" in shelves_lower:
        return "Non-Fiction"
        
    return "Non-Fiction"

def extract_tags(shelves, exclusive_shelf):
    tags = []
    # Combine shelves
    raw_tags = [s.strip().lower() for s in shelves.split(',')]
    if exclusive_shelf:
        raw_tags.append(exclusive_shelf.strip().lower())
        
    # Clean and unique tags
    for t in raw_tags:
        t_clean = t.replace('"', '').replace("'", "").strip()
        if t_clean and t_clean not in tags:
            tags.append(t_clean)
    return tags

def is_draft_file(filepath):
    if not os.path.exists(filepath):
        return True
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # If draft: true is present, it's a draft
            if "draft: true" in content:
                return True
    except Exception:
        pass
    return False

def main():
    csv_filename = "goodreads_export.csv"
    if len(sys.argv) > 1:
        csv_filename = sys.argv[1]
        
    if not os.path.exists(csv_filename):
        print(f"Error: CSV file '{csv_filename}' not found.")
        sys.exit(1)
        
    output_dir = "content/books"
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    overwritten = 0
    skipped = 0
    
    with open(csv_filename, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("Title", "").strip()
            book_id = row.get("Book Id", "").strip()
            
            if not title or not book_id:
                continue
                
            title_clean = clean_title(title)
            slug = slugify(title_clean)
            if not slug:
                slug = f"book-{book_id}"
                
            # Trim overly long slugs to match generating script
            if len(slug) > 60:
                parts = slug.split('-')[:5]
                slug = '-'.join(parts)
                
            filepath = os.path.join(output_dir, f"{slug}.md")
            
            # Check if file exists and whether we can overwrite it
            file_exists = os.path.exists(filepath)
            if file_exists:
                if not is_draft_file(filepath):
                    print(f"Skipped (published/non-draft): {filepath}")
                    skipped += 1
                    continue
                else:
                    overwritten += 1
            else:
                count += 1
                
            # Process authors
            author = row.get("Author", "").strip()
            additional_authors = row.get("Additional Authors", "").strip()
            authors = [author]
            if additional_authors:
                for aa in additional_authors.split(','):
                    aa_clean = aa.strip()
                    if aa_clean and aa_clean not in authors:
                        authors.append(aa_clean)
            
            # Extract tags from shelves
            shelves = row.get("Bookshelves", "")
            exclusive_shelf = row.get("Exclusive Shelf", "")
            tags = extract_tags(shelves, exclusive_shelf)
            
            # Map categories using smart rule-based classifier
            category = classify_book(title_clean, authors, shelves, exclusive_shelf)
            
            # Rating
            rating_str = row.get("My Rating", "0").strip()
            try:
                rating = int(rating_str)
                if rating == 0:
                    rating = "null"
            except ValueError:
                rating = "null"
                
            # Goodreads URL
            goodreads_url = f"https://www.goodreads.com/book/show/{book_id}"
            
            # Generate markdown content
            title_escaped = title_clean.replace('"', '\\"')
            md_content = f"""---
title: "{title_escaped}"
book_authors: {repr(authors)}
book_categories: ["{category}"]
link: "{goodreads_url}"
rating: {rating}
tags: {repr(tags)}
featured: false
draft: true
---

Draft page for *{title_clean}* by {', '.join(authors)}.
"""
            with open(filepath, "w", encoding="utf-8") as out:
                out.write(md_content)
                
            # print(f"Wrote draft: {filepath}")
            
    print(f"\nImport Summary:")
    print(f"  - Newly Created: {count} draft book pages")
    print(f"  - Overwritten/Updated: {overwritten} draft book pages")
    print(f"  - Skipped (published): {skipped} pages")

if __name__ == "__main__":
    main()
