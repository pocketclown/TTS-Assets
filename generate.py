from pathlib import Path
import html, json
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / 'images'
EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
files = sorted((p for p in IMAGES.rglob('*') if p.is_file() and p.suffix.lower() in EXTS), key=lambda p: p.name.casefold())
items = [{'name': p.stem.replace('_', ' ').replace('-', ' '), 'path': '/'.join(quote(part) for part in p.relative_to(ROOT).parts)} for p in files]
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TTS Asset Library</title><style>
:root{color-scheme:dark;font-family:system-ui,sans-serif}body{margin:0;background:#10121a;color:#f4f4f7}main{max-width:1150px;margin:auto;padding:36px 22px}h1{margin:0 0 8px;font-size:2rem}p{color:#aeb3c5}input{box-sizing:border-box;width:100%;padding:14px 16px;margin:18px 0 24px;border:1px solid #42475c;border-radius:12px;background:#1b1f2c;color:white;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px}.tile{cursor:pointer;background:#202432;border:1px solid #353a4d;border-radius:13px;overflow:hidden;color:inherit;text-align:left;padding:0;font:inherit;transition:transform .12s,border-color .12s}.tile:hover{transform:translateY(-3px);border-color:#b39aff}.tile img{display:block;width:100%;height:165px;object-fit:contain;background:#151824}.label{padding:12px;overflow-wrap:anywhere}.hint{display:block;color:#aeb3c5;font-size:.8rem;margin-top:5px}#toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#51408c;color:white;padding:12px 20px;border-radius:10px;display:none}#empty{display:none}
</style></head><body><main><h1>✦ TTS Asset Library</h1><p>Click any image to copy its direct URL for Tabletop Simulator.</p><input id="search" type="search" placeholder="Search your artwork…" aria-label="Search artwork"><div id="grid" class="grid"></div><p id="empty">No matching images found.</p></main><div id="toast" role="status"></div><script>
const assets = __ASSETS__;
const grid = document.querySelector('#grid');
const search = document.querySelector('#search');
const toast = document.querySelector('#toast');
function urlFor(path) { return new URL(path, document.baseURI).href; }
async function copyAsset(path) {
  const url = urlFor(path);
  try { await navigator.clipboard.writeText(url); toast.textContent = 'Copied image URL!'; }
  catch { toast.textContent = 'Clipboard unavailable. Copy this URL: ' + url; }
  toast.style.display = 'block';
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => toast.style.display = 'none', 3500);
}
function render() {
  grid.replaceChildren();
  const filtered = assets.filter(a => a.name.toLowerCase().includes(search.value.toLowerCase()));
  document.querySelector('#empty').style.display = filtered.length ? 'none' : 'block';
  for (const asset of filtered) {
    const button = document.createElement('button'); button.className = 'tile'; button.type = 'button';
    const img = document.createElement('img'); img.src = asset.path; img.alt = asset.name; img.loading = 'lazy';
    const label = document.createElement('div'); label.className = 'label'; label.textContent = asset.name;
    const hint = document.createElement('span'); hint.className = 'hint'; hint.textContent = 'Click to copy URL'; label.append(hint);
    button.append(img, label); button.addEventListener('click', () => copyAsset(asset.path)); grid.append(button);
  }
}
search.addEventListener('input', render); render();
</script></body></html>'''
(ROOT / 'index.html').write_text(page.replace('__ASSETS__', json.dumps(items).replace('</', '<\\/')), encoding='utf-8')
print(f'Generated index.html with {len(items)} images')
