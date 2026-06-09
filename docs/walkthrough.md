# Walkthrough - Goodreads Integration, Book Sorting, Blog Section & Category Visibility Harmonization

All tasks have been successfully completed! Below is a summary of the features, styling enhancements, layout optimizations, and local verification results.

## Changes Made

### 1. Created Bulk Goodreads CSV Import Utility
- **File**: [import_goodreads_csv.py](file:///Users/akarsh/Documents/Personal%20Website/personal_website/scripts/import_goodreads_csv.py)
- **Features**: 
  - Converts a Goodreads `.csv` library export (from "My Books" -> "Tools" -> "Export Library") into Hugo draft pages.
  - Formats author lists, parses user ratings, handles URL mapping, and slugifies book titles.
  - Skips already existing files to preserve manual updates/edits.

### 2. Pre-Populated and Imported All Goodreads Books
- Generated **338 markdown draft pages** in `content/books/` from your library export CSV file (`goodreads_library_export.csv`).
- Each file includes the title, authors, mapped categories, direct Goodreads link, rating (from Goodreads), and a `draft: true` status.

### 3. Harmonized Book & Blog Category Heading Styles
- **File**: [custom.css](file:///Users/akarsh/Documents/Personal%20Website/personal_website/static/css/custom.css)
- **Features**:
  - Replaced the bootstrap-default blue and general link-override red heading colors on both the **Books** and **Blogs** category lists with the theme's core heading black (`#000000`).
  - Matched headings with the homepage font size rules: `32px` on mobile, scaling up to `48px` on desktop (screens with `min-width: 992px`) using font family `Inter` and weight `700`.
  - Configured the links to hover smoothly into the theme red (`#e93e34`).
  - Removed the chain icon (`🔗`) from headers on both the Blog and Books index files.

### 4. Advanced Pagination: Step-by-Step, Expand All, and Collapse
- **Files**:
  - [book-summary.html](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/partials/book-summary.html)
  - [blog-summary.html](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/partials/blog-summary.html)
  - [list.html (books)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/books/list.html)
  - [single.html (books)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/books/single.html)
  - [list.html (blog)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/blog/list.html)
- **Features**:
  - The books and blogs list pages show **5 items by default** under each category.
  - If there are more than 5 items, a control panel is rendered with options to show next 5, show all, or collapse back to top.

### 5. Goodreads Link Icon & Dynamic Bookshelf Tags in Header
- **File**: [book-summary.html](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/partials/book-summary.html)
- **Features**:
  - Positioned the Goodreads logo icon directly **after (following) the book title**.
  - Hyperlinked **only the icon** to Goodreads. The title itself is rendered as clean, plain text.
  - Used the **exact same outline SVG icon** from your homepage's social section (rounded square with a lowercase 'g') for visual consistency.
  - Placed the **bookshelf tag links directly next to the Goodreads icon inside the h5 header** line.
  - Styled these tag badges using subtle grey color by default (`#6c757d`) and transition to theme red (`#e93e34`) on hover.
  - Configured custom SVG outline stroke color styles: the icon has a stroke of `#000000` (black) and an opacity of `0.6` by default, scaling up (`transform: scale(1.15)`) and fading to a stroke of `#e93e34` (theme red) at `1.0` opacity on hover.

### 6. Hyperlinked Book Authors & Cleaned Formatting
- **Files**:
  - [book-summary.html](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/partials/book-summary.html)
  - [config.toml](file:///Users/akarsh/Documents/Personal%20Website/personal_website/config.toml) (Added custom taxonomy configuration)
  - [book_author.html](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/taxonomy/book_author.html) (New taxonomy term list template)
  - [custom.css](file:///Users/akarsh/Documents/Personal%20Website/personal_website/static/css/custom.css)
- **Features**:
  - Removed the leading comma before the author name (`", by [Authors]"` changed to `"by [Authors]"`).
  - Hyperlinked each individual author name to an automatically generated page (`/book_authors/<author-slug>/`) listing all books by that author.
  - Styled these links to be red by default and transition to black on hover to provide feedback.

### 7. Smart Book Classifier & Custom Sorting order
- **Files**:
  - [import_goodreads_csv.py](file:///Users/akarsh/Documents/Personal%20Website/personal_website/scripts/import_goodreads_csv.py)
  - [list.html (books)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/books/list.html)
  - [single.html (books)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/books/single.html)
- **Features**:
  - **Smart Rule-Based Classifier**: Upgraded the script to categorize books into "Fiction", "Non-Fiction", "Philosophy", "Poetry" based on keywords/authors, and removed the redundant "My reading list" category (mapping fallbacks directly into "Non-Fiction").
  - **Sorting Order Fix**: Avoided Hugo's `union` automatic page collection sorting. Replaced it with sequential loops to build the final list by status:
    1. **currently-reading** (sorted alphabetically by Title)
    2. **read** (sorted alphabetically by Title)
    3. **to-read** (sorted alphabetically by Title)
    4. Fallbacks/others (sorted alphabetically by Title)
    5. **did-not-complete** (sorted alphabetically by Title, placed at the absolute end of the lists)

### 8. Category Visibility: Hiding Empty Categories
- **Files**:
  - [list.html (books)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/books/list.html)
  - [list.html (blog)](file:///Users/akarsh/Documents/Personal%20Website/personal_website/layouts/blog/list.html)
- **Features**:
  - Wrapped both book and blog category sections in an `if` block that checks for item count.
  - Category headers (`<h2>`) and list containers (`<ul>`) are only rendered if there is at least one book or post belonging to that category, hiding empty sections from view (e.g. hiding the three currently empty blog categories).

---

## Verification Results

We verified that:
1. **Compilation**: Running `hugo -D` compiles successfully with `Pages: 1128` (rendering all book draft pages, author pages, and tag listing pages).
2. **Category Harmonization & Hiding**: Checked that empty categories are successfully hidden. For the blog page, the categories "Product, strategy and business", "Leadership", and "Workplace and culture" are hidden because they contain zero posts, cleanly rendering only the "Mindless Musings" section.
3. **Pagination & Collapse**: Verified book listing categories limit display to 5 books, offering "Show Next 5", "Show All", and "Collapse" back to top.
4. **Shelf Sorting**: Verified using a local parser script that books are grouped strictly by status, starting with `currently-reading`, followed by `read`, `to-read`, and placing `did-not-complete` books at the absolute end.
5. **Tags and Author Links**: Checked that all links point to correct taxonomy paths (`/tags/<slug>/` and `/book_authors/<slug>/`) and render successfully.
