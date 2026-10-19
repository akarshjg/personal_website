import urllib.request
import re
import html

def main():
    url = "https://imginn.com/aio.wiz/"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8')
            
            # Locate all post divs/links in Imginn HTML
            # Typically structured as:
            # <div class="item">
            #   <a href="/p/C-abc/" ...>
            #     <img src="https://..." alt="caption text by @aio.wiz" ...>
            #   </a>
            # </div>
            
            # Let's find all instances of <div class="item"> blocks
            # Or scan for the <a> tag and the inner <img> tag.
            matches = re.finditer(r'<a\s+href="(/p/[^"]+)"[^>]*>.*?<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', html_content, re.DOTALL)
            
            results = []
            for i, match in enumerate(matches):
                post_path = match.group(1)
                img_url = match.group(2)
                alt_text = match.group(3)
                
                # Clean HTML entities in alt text
                alt_clean = html.unescape(alt_text).strip()
                # Clean up "by @aio.wiz" or similar from the caption if present
                caption = re.sub(r'\s*by\s*@\w+\s*$', '', alt_clean, flags=re.IGNORECASE).strip()
                
                permalink = f"https://www.instagram.com{post_path}"
                img_url_clean = html.unescape(img_url)
                
                results.append({
                    "id": f"insta-{i}",
                    "mediaUrl": img_url_clean,
                    "permalink": permalink,
                    "caption": caption or "Captured moment.",
                    "mediaType": "IMAGE"
                })
                
            print(f"Parsed {len(results)} posts successfully!")
            for idx, post in enumerate(results[:3]):
                print(f"Post {idx+1}:")
                print(f"  ID: {post['id']}")
                print(f"  URL: {post['permalink']}")
                print(f"  Image: {post['mediaUrl']}")
                print(f"  Caption: {post['caption']}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
