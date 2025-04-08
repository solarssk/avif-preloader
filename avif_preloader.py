import requests
import xml.etree.ElementTree as ET
import time
from bs4 import BeautifulSoup
from collections import Counter

# Headers to simulate a browser that supports AVIF
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
}

# Stats and image list
image_stats = Counter()
all_images = []

def get_urls_from_sitemap(sitemap_url):
    print(f"\n📥 Downloading sitemap: {sitemap_url}")
    
    try:
        r = requests.get(sitemap_url)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching sitemap: {e}")
        return []

    try:
        root = ET.fromstring(r.content)
    except ET.ParseError:
        print("❌ This doesn't look like a valid XML sitemap.")
        print("ℹ️  Please check the URL and run the script again.")
        return []

    urls = []
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    for sm in root.findall("ns:sitemap", ns):
        loc = sm.find("ns:loc", ns)
        if loc is not None:
            urls.extend(get_urls_from_sitemap(loc.text))

    for url in root.findall("ns:url", ns):
        loc = url.find("ns:loc", ns)
        if loc is not None:
            urls.append(loc.text)

    return urls

def check_images_on_page(page_url):
    global image_stats, all_images

    try:
        print(f"\n🌐 Scanning page: {page_url}")
        res = requests.get(page_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        imgs = soup.find_all('img')

        if not imgs:
            print("   ⚠️  No images found.")
            return

        for img in imgs:
            src = img.get('src')
            if not src or not src.startswith("http"):
                continue

            try:
                img_res = requests.get(src, headers=HEADERS, timeout=10, stream=True)
                content_type = img_res.headers.get('Content-Type', '').lower()

                if 'avif' in content_type:
                    image_stats['AVIF'] += 1
                    print(f"   ✅ AVIF: {src}")
                elif 'webp' in content_type:
                    image_stats['WebP'] += 1
                    print(f"   🟡 WebP: {src}")
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    image_stats['JPEG'] += 1
                    print(f"   🔵 JPEG: {src}")
                elif 'png' in content_type:
                    image_stats['PNG'] += 1
                    print(f"   🟠 PNG: {src}")
                else:
                    image_stats['Other'] += 1
                    print(f"   ⚪ Other ({content_type}): {src}")

                all_images.append((src, content_type))

            except Exception as e:
                print(f"   ❌ Error loading image: {src} ({e})")
                image_stats['Errors'] += 1

    except Exception as e:
        print(f"   ❌ Error loading page: {page_url} ({e})")

def main():
    try:
        sitemap_url = input("🌐 Enter your sitemap URL: ").strip()

        if not sitemap_url.startswith("http"):
            print("❌ Invalid URL. Must start with http or https.")
            print("ℹ️  Please run the script again and provide a valid sitemap URL.")
            return

        urls = get_urls_from_sitemap(sitemap_url)

        if not urls:
            print("⚠️  No valid URLs found in the sitemap.")
            print("ℹ️  Please check the sitemap URL and run the script again.")
            return

        print(f"\n🔍 Checking {len(urls)} pages...\n")
        for url in urls:
            check_images_on_page(url)
            time.sleep(1)

        total = sum(image_stats.values())

        print("\n📊 SUMMARY:")
        print(f"   🔢 Total images found: {total}")
        for k, v in image_stats.items():
            print(f"   - {k}: {v}")

    except KeyboardInterrupt:
        print("\n🚫 Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()