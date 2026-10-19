import urllib.request
import re

def main():
    url = "https://imginn.com/aio.wiz/"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            print("Successfully loaded Imginn page!")
            print(f"HTML length: {len(html)}")
            
            # Find photo URLs
            # Imginn typically wraps posts in a container with img tags
            images = re.findall(r'src="(https://[^"]+)"', html)
            print(f"Found {len(images)} image URLs.")
            for img in images[:10]:
                print(img)
                
            # Let's search for actual post items in html
            items = re.findall(r'<div class="item">.*?<img.*?src="([^"]+)".*?alt="([^"]*)"', html, re.DOTALL)
            print(f"Found {len(items)} items with alt tags.")
            for src, alt in items[:3]:
                print(f"  Src: {src}")
                print(f"  Alt: {alt}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
