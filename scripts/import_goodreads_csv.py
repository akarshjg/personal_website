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

def get_existing_tags(front_matter):
    # Try inline format: tags: ['a', 'b']
    inline_match = re.search(r'tags:\s*\[(.*?)\]', front_matter)
    if inline_match:
        return [t.strip().strip("'").strip('"') for t in inline_match.group(1).split(',') if t.strip()]
    
    # Try block format:
    # tags:
    #   - a
    #   - b
    lines = front_matter.split('\n')
    tags = []
    in_tags = False
    for line in lines:
        if line.strip().startswith('tags:'):
            in_tags = True
            continue
        if in_tags:
            # If we hit another key, stop
            if line.strip() and not line.strip().startswith('-'):
                break
            if line.strip().startswith('-'):
                tag_val = line.replace('-', '', 1).strip().strip("'").strip('"')
                tags.append(tag_val)
    return tags

def update_front_matter_tags(front_matter, new_tags):
    lines = front_matter.split('\n')
    new_lines = []
    in_tags_block = False
    tags_inserted = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('tags:'):
            new_lines.append(f"tags: {repr(new_tags)}")
            tags_inserted = True
            # If it's a block format, we want to skip subsequent block items
            if not stripped.endswith(']'):
                in_tags_block = True
            continue
            
        if in_tags_block:
            if stripped.startswith('-'):
                # Skip this block item
                continue
            else:
                in_tags_block = False
                
        new_lines.append(line)
        
    if not tags_inserted:
        new_lines.append(f"tags: {repr(new_tags)}")
        
    return '\n'.join(new_lines)

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
            
            # Check if file exists and whether we can sync tags
            file_exists = os.path.exists(filepath)
            if file_exists:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f_in:
                        existing_content = f_in.read()
                    
                    parts = existing_content.split('---', 2)
                    if len(parts) >= 3:
                        front_matter = parts[1]
                        body = parts[2]
                        
                        # Extract book ID from link in front matter to check if it matches this edition
                        link_match = re.search(r'link:\s*"(.*?)"', front_matter)
                        if link_match:
                            existing_link = link_match.group(1)
                            existing_book_id_match = re.search(r'/show/(\d+)', existing_link)
                            if existing_book_id_match:
                                existing_book_id = existing_book_id_match.group(1)
                                if existing_book_id != book_id:
                                    # This is a different edition of the same book, skip to avoid overwriting tags
                                    skipped += 1
                                    continue
                        
                        existing_tags = get_existing_tags(front_matter)
                        if set(existing_tags) == set(tags):
                            # No change in tags, skip completely
                            skipped += 1
                            continue
                        
                        # Update tags in front matter
                        new_front_matter = update_front_matter_tags(front_matter, tags)
                        new_content = parts[0] + '---' + new_front_matter + '---' + body
                        
                        with open(filepath, 'w', encoding='utf-8') as f_out:
                            f_out.write(new_content)
                        
                        print(f"Updated tags: {filepath}")
                        overwritten += 1
                        continue
                except Exception as ex:
                    print(f"Error updating tags for {filepath}: {ex}")
                
                skipped += 1
                continue
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
