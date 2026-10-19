import urllib.request
import re

def main():
    url = "https://www.picuki.com/profile/aio.wiz"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            print("Successfully loaded Picuki page!")
            print(f"HTML length: {len(html)}")
            
            # Look for photo links
            # Picuki lists posts under images with class "post-image" or similar
            # E.g. <img class="post-image" src="..."
            images = re.findall(r'src="(https://scontent[^"]+)"', html)
            print(f"Found {len(images)} scontent images.")
            for img in images[:5]:
                print(img)
                
            # Or check for post links
            posts = re.findall(r'href="(https://www.picuki.com/media/[^"]+)"', html)
            print(f"Found {len(posts)} media links.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
