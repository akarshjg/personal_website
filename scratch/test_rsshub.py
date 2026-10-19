import urllib.request
import json
import ssl

def main():
    # Disable SSL verification for testing public instances
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    instances = [
        "https://rsshub.app",
        "https://rsshub.diygod.me",
        "https://rss.owo.best",
        "https://rsshub.feed.plus"
    ]
    
    for base in instances:
        url = f"{base}/instagram/user/aio.wiz.json"
        print(f"Testing instance: {url}")
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
                data = response.read().decode('utf-8')
                feed = json.loads(data)
                items = feed.get("items", [])
                print(f"-> Success! Found {len(items)} items.")
                if items:
                    for i, item in enumerate(items[:3]):
                        print(f"Item {i+1}:")
                        print(f"  Title: {item.get('title')}")
                        print(f"  Url: {item.get('url')}")
                        print(f"  Image: {item.get('image') or item.get('banner')}")
                    return
        except Exception as e:
            print(f"-> Failed: {e}")

if __name__ == "__main__":
    main()
