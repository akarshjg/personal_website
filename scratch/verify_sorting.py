import urllib.request
import re

url = "http://127.0.0.1:1313/books/"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    
    # Let's split by category using the <h2 heading
    categories = re.split(r'<h2 [^>]*class="[^"]*book-category[^"]*"[^>]*>', html)
    print(f"Found {len(categories)-1} categories.")
    
    for idx, cat_html in enumerate(categories[1:], 1):
        # Find category name
        cat_name_match = re.search(r'id="([^"]+)"', cat_html)
        cat_name = cat_name_match.group(1) if cat_name_match else f"Category {idx}"
        print(f"\nCategory: {cat_name}")
        
        # Find all li.book-content
        books = re.findall(r'<li class="book-content[^"]*".*?</li>', cat_html, re.DOTALL)
        total = len(books)
        print(f"  Total books found: {total}")
        
        # Print the last 10 books in this category to see if did-not-complete are at the end
        start_idx = max(0, total - 10)
        for j, book in enumerate(books[start_idx:], start_idx + 1):
            title_match = re.search(r'<h5 class="book-title".*?<span>(.*?)</span>', book, re.DOTALL)
            title = "Unknown"
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                title = " ".join(title.split())
            
            # check tags
            tags = re.findall(r'#([a-zA-Z0-9-]+)', book)
            print(f"    {j}. {title} -- Tags: {tags}")
            
except Exception as e:
    print("Error fetching/parsing page:", e)
