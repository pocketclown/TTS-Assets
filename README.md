# TTS Asset Library

A simple, static GitHub Pages image gallery. Clicking an image copies its direct URL.

## Add images

Put `.png`, `.jpg`, `.jpeg`, `.webp`, or `.gif` files in the `images/` directory. Subfolders are supported.

Run:

```bash
python generate.py
```

This rebuilds `index.html` using all image files it finds. Run it again after adding or removing images.

## Test locally

```bash
python -m http.server 8000
```

Visit `http://localhost:8000`. Thumbnails work locally; **copied URLs will be localhost URLs until published on GitHub Pages**, so use the published site when copying URLs for TTS.

## Publish with GitHub Pages

1. Create a **public** GitHub repository, e.g. `tts-assets`.
2. Push these files to its `main` branch (including the `images/` directory and generated `index.html`).
3. On GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → main → / (root) → Save**.
4. Visit `https://YOUR_USERNAME.github.io/tts-assets/` after deployment finishes.
5. Click a thumbnail to copy the public direct image URL, e.g. `https://YOUR_USERNAME.github.io/tts-assets/images/massacre-girl.png`.

**Note:** Keep the repository public for public image URLs. GitHub Pages has usage limits; it is not a guaranteed high-volume CDN. Test one image in TTS before migrating everything.
