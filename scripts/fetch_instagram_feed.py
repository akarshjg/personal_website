#!/usr/bin/env python3
import urllib.request
import re
import html
import json
import os
import ssl

def main():
    username = "aio.wiz"
    url = f"https://imginn.com/{username}/"
    output_filepath = "data/photography.json"
    
    print(f"Fetching Instagram feed for @{username} from Imginn...")
    
    # Disable SSL certificate verification (needed for some build container environments)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as response:
            html_content = response.read().decode('utf-8')
            
            # Match <a> tag links to posts and inner <img> tags
            matches = re.finditer(r'<a\s+href="(/p/[^"]+)"[^>]*>.*?<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', html_content, re.DOTALL)
            
            photography_list = []
            for i, match in enumerate(matches):
                post_path = match.group(1)
                img_url = match.group(2)
                alt_text = match.group(3)
                
                # Unescape HTML entities
                alt_clean = html.unescape(alt_text).strip()
                img_url_clean = html.unescape(img_url)
                
                # Reconstruct direct Instagram CDN URL to bypass proxy CORP (Cross-Origin Resource Policy) blocks
                direct_url = img_url_clean
                url_match = re.search(r'\?([^/]+)/([^?]+)\?(.*)$', img_url_clean)
                if url_match:
                    folder = url_match.group(1)
                    filename = url_match.group(2)
                    query = url_match.group(3)
                    host_match = re.search(r'_nc_ht=([^&]+)', query)
                    host = host_match.group(1) if host_match else 'scontent-atl3-2.cdninstagram.com'
                    direct_url = f"https://{host}/v/{folder}/{filename}?{query}"
                
                # Clean up "by @aio.wiz" or similar from the end of the caption
                caption = re.sub(r'\s*by\s*@[\w.]+\s*$', '', alt_clean, flags=re.IGNORECASE).strip()
                
                permalink = f"https://www.instagram.com{post_path}"
                
                photography_list.append({
                    "id": f"insta-{i}",
                    "mediaUrl": direct_url,
                    "permalink": permalink,
                    "caption": caption or "Captured moment.",
                    "mediaType": "IMAGE"
                })
                
            if photography_list:
                os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
                with open(output_filepath, "w", encoding="utf-8") as f:
                    json.dump(photography_list, f, indent=2, ensure_ascii=False)
                print(f"Successfully scraped Instagram feed! Wrote {len(photography_list)} posts to {output_filepath}")
            else:
                print("Failed to parse any posts from the page. Retaining existing data.")
                
    except Exception as e:
        print(f"Error scraping Instagram feed: {e}")
        print("Build will proceed using existing/fallback data.")

if __name__ == "__main__":
    main()
