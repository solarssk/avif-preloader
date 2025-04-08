# 🖼️ AVIF Checker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/github/license/solarssk/avif-checker?style=flat-square)

> A fast, sitemap-based AVIF preloader and image format scanner for WordPress and static sites.

---

## 🚀 What does it do?

This script:

- Crawls your entire site using `sitemap.xml`
- Finds all `<img>` tags on each page
- Sends AVIF-compatible headers to trigger image generation (AVIF, WebP, JPEG, PNG)
- Logs image formats for caching/CDN inspection (e.g. Cloudflare, EWWW)
- Outputs a summary by MIME type

---

## ⚙️ Setup & Usage

### 🔧 Option 1: Run with auto-setup

```
bash
./setup.sh
```

This script will:
- Check if python3 and pip3 are available
- Install required libraries
- Launch the checker

### 🧪 Option 2: Manual steps

```
pip3 install -r requirements.txt
python3 avif_checker.py
```

You will be prompted to enter your sitemap URL, for example:

```
🌐 Enter your sitemap URL: https://example.com/sitemap_index.xml
```

### 📊 Output Example

```
📊 SUMMARY:
   🔢 Total images found: 87
   - AVIF: 43
   - WebP: 21
   - JPEG: 20
   - PNG: 3
```

## 💡 Why this exists?

If you're using a free Cloudflare plan, you have **limited control over how dynamic content is cached**.  
Image optimization plugins (like EWWW, Optimole, ShortPixel, or LiteSpeed) often **generate AVIF/WebP on-the-fly** — only when requested with proper headers.

On the first request:
- The AVIF version is generated
- But it might **not be cached immediately by Cloudflare**
- Users experience delays or see fallback formats like JPEG

This script solves that by:
- Visiting each image with an AVIF-compatible `Accept` header
- Forcing dynamic formats to be generated
- Helping to **preload and "warm up" the CDN cache**, even on free Cloudflare plans

## 🛠️ To Do

- Export to CSV
- Add CLI arguments for headless mode
- Improve parallelism for large sites

## 📄 License
MIT – use it, fork it, improve it 🙌
