#!/usr/bin/env python3
"""
JOKESSHOTS Site Builder
Processes photos and generates HTML pages from folder structure.
"""

import os
import shutil
import json
from PIL import Image
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────

BASE = Path("/home/jeffjanovitch/claude-projects/jokesshots")
NEW_PHOTOS = BASE / "new-photos"
SRC = BASE / "src"
ASSETS = SRC / "assets" / "photos"
PAGES_DIR = SRC / "pages"

# Photo processing tiers
TIERS = {
    "thumbs": {"width": 400, "quality": 70},
    "medium": {"width": 1200, "quality": 80},
    "full":   {"width": 1920, "quality": 85},
}

# ── Page definitions ───────────────────────────────────────────────

PAGES = [
    # Concerts
    {"slug": "boon", "title": "Boondawg", "subtitle": "Kultmania — Live Music Hall Köln", "category": "concert", "folder": "Concerts/boon",
     "videos": [{"id": "2yywxFtws8g", "title": "Kultmania Live Music Hall — Listening Event von Boondawg"}]},
    {"slug": "concert-misc", "title": "Concert Misc", "subtitle": "Mixed Concert Photography", "category": "concert", "folder": "Concerts/concert misc",
     "videos": [
         {"id": "Q1URlfSeu0M", "title": "LFDY presents Metro Boomin — Rheinriff Düsseldorf"},
         {"id": "tLqxDslR7Ss", "title": "JID — E-Werk Köln"},
         {"id": "Pm4yBjrYZ8U", "title": "Larry June — CBE Köln"},
     ]},
    {"slug": "cube", "title": "Ice Cube", "subtitle": "Live Performance", "category": "concert", "folder": "Concerts/cube", "videos": []},
    {"slug": "fabolous", "title": "Fabolous", "subtitle": "Preact für Nelly — Oberhausen", "category": "concert", "folder": "Concerts/fabolous",
     "videos": [{"id": "J8mqkHg-U8A", "title": "Fabolous als Preact für Nelly in Oberhausen"}]},
    {"slug": "hype", "title": "Hypefestival", "subtitle": "Festival Coverage", "category": "concert", "folder": "Concerts/hype",
     "videos": [
         {"id": "VmQJu8pPHeY", "title": "Hypefestival 2024 Recap"},
         {"id": "FDAQp-FtyQo", "title": "Hypefestival 2025 Recap"},
     ]},
    {"slug": "kaytra", "title": "Kaytranada", "subtitle": "Timeless Tour — Palladium Köln", "category": "concert", "folder": "Concerts/kaytra",
     "videos": [{"id": "26Dn3xE0QE8", "title": "Kaytranada Timeless Tour — Palladium Köln"}]},
    {"slug": "loboda", "title": "Loboda", "subtitle": "Live Performance", "category": "concert", "folder": "Concerts/loboda", "videos": []},
    {"slug": "ogkeemo", "title": "OG Keemo", "subtitle": "Live Performance", "category": "concert", "folder": "Concerts/ogkeemo",
     "videos": [{"id": "hLKZIXKxO6g", "title": "OG Keemo Recap"}]},
    {"slug": "summerjam", "title": "Summerjam", "subtitle": "Festival Coverage", "category": "concert", "folder": "Concerts/summerjam",
     "videos": [
         {"id": "oc30gzro7XM", "title": "Summerjam 2024 Festival Recap"},
         {"id": "PjKjpxL3_UA", "title": "Summerjam 2025 Festival Recap"},
     ]},
    {"slug": "unreleased", "title": "Unreleased", "subtitle": "Concert Photography", "category": "concert", "folder": "Concerts/unreleased", "videos": []},
    # Events
    {"slug": "icon-league", "title": "Icon League", "subtitle": "Castello Düsseldorf", "category": "event", "folder": "Events/icon league",
     "videos": [{"id": "zZcJHMNbvQo", "title": "Icon League — Castello Düsseldorf"}]},
    {"slug": "harlem-globe", "title": "Harlem Globetrotters", "subtitle": "Castello Düsseldorf", "category": "event", "folder": "Events/harlem globe",
     "videos": [{"id": "P-YxQnLncOM", "title": "Harlem Globetrotters — Castello Düsseldorf"}]},
    {"slug": "dancebattle", "title": "Area UDC Dancebattle", "subtitle": "Dance Competition", "category": "event", "folder": "Events/area udc dancebattle",
     "videos": [{"id": "yDUvLG80rvY", "title": "UDC Dancebattle 2025 Recap"}]},
    {"slug": "event-misc", "title": "Event Misc", "subtitle": "Mixed Event Coverage", "category": "event", "folder": "Events/event misc", "videos": []},
    {"slug": "sport", "title": "Sport", "subtitle": "WeLoveMMA & More", "category": "event", "folder": "Events/sport",
     "videos": [{"id": "8shSCf--5Jc", "title": "WeLoveMMA Berlin 2024 — Debüt Frederic Vosgrüne"}]},
    # Fashion
    {"slug": "afw", "title": "African Fashion Week", "subtitle": "Fashion Photography", "category": "fashion", "folder": "Events/afw", "videos": []},
    {"slug": "sourire", "title": "Sourire", "subtitle": "Fashion Editorial", "category": "fashion", "folder": "sourire", "videos": []},
    # Portraits / Urban / Other
    {"slug": "portraits", "title": "Portraits", "subtitle": "Portrait Photography", "category": "portrait", "folder": "Portraits", "videos": []},
    {"slug": "urban", "title": "Urban", "subtitle": "Street Photography", "category": "urban", "folder": "Urban", "videos": []},
    {"slug": "shooting-misc", "title": "Shooting Misc", "subtitle": "Mixed Shoots", "category": "portrait", "folder": "Shooting misc", "videos": []},
    {"slug": "tattoo", "title": "Tattoo", "subtitle": "Tattoo Photography", "category": "portrait", "folder": "tattoo", "videos": []},
]

# Category labels for display
CATEGORY_LABELS = {
    "concert": "Concert",
    "event": "Event",
    "fashion": "Fashion",
    "portrait": "Portrait",
    "urban": "Urban",
}

# ── Photo Processing ───────────────────────────────────────────────

def process_photos():
    """Process all photos into thumb/medium/full JPEG tiers."""
    print("\n=== PROCESSING PHOTOS ===\n")

    # Clean old photo directories (keep about/ for now)
    for tier in TIERS:
        tier_dir = ASSETS / tier
        if tier_dir.exists():
            shutil.rmtree(tier_dir)

    total = 0
    for page in PAGES:
        src_folder = NEW_PHOTOS / page["folder"]
        if not src_folder.exists():
            print(f"  SKIP {page['slug']}: folder not found at {src_folder}")
            continue

        photos = sorted([
            f for f in src_folder.iterdir()
            if f.suffix.lower() in ('.png', '.jpg', '.jpeg')
        ])

        if not photos:
            print(f"  SKIP {page['slug']}: no photos found")
            continue

        print(f"  {page['slug']}: {len(photos)} photos")

        for tier_name, tier_cfg in TIERS.items():
            out_dir = ASSETS / tier_name / page["slug"]
            out_dir.mkdir(parents=True, exist_ok=True)

            for photo in photos:
                out_name = photo.stem + ".jpg"
                out_path = out_dir / out_name

                if out_path.exists():
                    continue

                try:
                    img = Image.open(photo)
                    img = img.convert("RGB")

                    # Resize maintaining aspect ratio
                    w, h = img.size
                    target_w = tier_cfg["width"]
                    if w > target_w:
                        ratio = target_w / w
                        new_size = (target_w, int(h * ratio))
                        img = img.resize(new_size, Image.LANCZOS)

                    # Save as progressive JPEG
                    img.save(out_path, "JPEG",
                             quality=tier_cfg["quality"],
                             progressive=True,
                             optimize=True)
                    total += 1
                except Exception as e:
                    print(f"    ERROR processing {photo.name}: {e}")

    print(f"\n  Total images processed: {total}")


def get_photos_for_page(page):
    """Get sorted list of photo filenames (as .jpg) for a page."""
    src_folder = NEW_PHOTOS / page["folder"]
    if not src_folder.exists():
        return []

    photos = sorted([
        f.stem + ".jpg"
        for f in src_folder.iterdir()
        if f.suffix.lower() in ('.png', '.jpg', '.jpeg')
    ])
    return photos


def get_titelbild(page):
    """Find the TITELBILD photo for a page, or return the first photo."""
    src_folder = NEW_PHOTOS / page["folder"]
    if not src_folder.exists():
        return None

    # Look for titel/TITELBILD marker
    for f in src_folder.iterdir():
        if "titel" in f.name.lower() and f.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            return f.stem + ".jpg"

    # Fallback: first photo
    photos = get_photos_for_page(page)
    return photos[0] if photos else None


# ── HTML Generation ────────────────────────────────────────────────

def generate_video_embed_html(videos):
    """Generate YouTube video embed section."""
    if not videos:
        return ""

    embeds = []
    for v in videos:
        embeds.append(f'''                <div class="video-embed-item">
                    <div class="video-embed-wrap">
                        <iframe src="https://www.youtube.com/embed/{v['id']}" title="{v['title']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
                    </div>
                    <p class="video-embed-title">{v['title']}</p>
                </div>''')

    return f'''
    <section class="project-videos">
        <div class="container">
            <h3 class="project-videos-heading">Recaps</h3>
            <div class="video-embed-grid">
{chr(10).join(embeds)}
            </div>
        </div>
    </section>
'''


def generate_page_html(page, next_page=None):
    """Generate full HTML for a project page."""
    slug = page["slug"]
    title = page["title"]
    subtitle = page["subtitle"]
    category = CATEGORY_LABELS.get(page["category"], page["category"])
    photos = get_photos_for_page(page)
    titelbild = get_titelbild(page)
    hero_img = titelbild or (photos[0] if photos else "placeholder.jpg")

    # Filter out titelbild from gallery if it's used as hero
    # Actually keep all photos in gallery — hero is just the cover

    # Build photo grid
    photo_items = []
    for i, photo in enumerate(photos):
        # Make every 4th photo wide for visual variety
        wide_class = ' project-photo--wide' if (i % 5 == 3) else ''
        photo_items.append(f'''                <div class="project-photo{wide_class}" data-full="../assets/photos/full/{slug}/{photo}">
                    <img src="../assets/photos/medium/{slug}/{photo}" alt="{title}" loading="lazy">
                </div>''')

    photo_grid = "\n".join(photo_items)

    # Video embeds
    video_section = generate_video_embed_html(page.get("videos", []))

    # Next project nav
    next_nav = ""
    if next_page:
        next_nav = f'''    <div class="project-nav">
        <a href="{next_page['slug']}.html" class="project-nav-link">
            <span class="project-nav-label" data-i18n="project.next">Next Project</span>
            <span class="project-nav-title">{next_page['title'].upper()}</span>
        </a>
    </div>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>{title} &mdash; JOKESSHOTS</title>
    <meta name="description" content="{title} — {subtitle}. Photography by JOKER.">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📷</text></svg>">
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="stylesheet" href="../css/project.css">
    <script src="../js/i18n.js"></script>
</head>
<body>

    <nav class="nav" id="nav">
        <a href="../index.html" class="nav-logo">JOKESSHOTS</a>
        <div class="nav-links" id="navLinks">
            <a href="../index.html#work" class="nav-link" data-i18n="nav.work">Work</a>
            <a href="../index.html#about" class="nav-link" data-i18n="nav.about">About</a>
            <a href="../index.html#contact" class="nav-link" data-i18n="nav.contact">Contact</a>
            <span class="lang-switcher">
                <button class="lang-option active" data-lang="en">EN</button>
                <span class="lang-divider">|</span>
                <button class="lang-option" data-lang="de">DE</button>
            </span>
            <a href="https://instagram.com/jokesshots" target="_blank" rel="noopener noreferrer" class="nav-link nav-link--social">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="5"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none"/></svg>
            </a>
        </div>
        <button class="nav-toggle" id="navToggle" aria-label="Menu">
            <span></span>
            <span></span>
        </button>
    </nav>

    <div class="mobile-menu" id="mobileMenu">
        <a href="../index.html#work" class="mobile-menu-link" data-i18n="mobile.work">Work</a>
        <a href="../index.html#about" class="mobile-menu-link" data-i18n="mobile.about">About</a>
        <a href="../index.html#contact" class="mobile-menu-link" data-i18n="mobile.contact">Contact</a>
        <a href="https://instagram.com/jokesshots" target="_blank" rel="noopener noreferrer" class="mobile-menu-link mobile-menu-link--small">Instagram</a>
        <div class="mobile-lang-switcher">
            <button class="lang-option active" data-lang="en">EN</button>
            <span class="lang-divider">|</span>
            <button class="lang-option" data-lang="de">DE</button>
        </div>
    </div>

    <section class="project-hero">
        <div class="project-hero-img">
            <img src="../assets/photos/full/{slug}/{hero_img}" alt="{title}">
        </div>
        <div class="project-hero-overlay"></div>
        <div class="project-hero-content">
            <a href="../index.html#work" class="project-back">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg>
                <span data-i18n="project.back">Back to Work</span>
            </a>
            <h1 class="project-title">{title}</h1>
            <span class="project-meta">{category} &mdash; {subtitle}</span>
        </div>
    </section>
{video_section}
    <section class="project-gallery">
        <div class="container">
            <div class="project-grid">
{photo_grid}
            </div>
        </div>
    </section>

{next_nav}
    <footer class="footer">
        <div class="container footer-inner">
            <span class="footer-copy" data-i18n="project.footer">&copy; 2026 JOKESSHOTS. All rights reserved.</span>
            <div class="footer-links">
                <a href="https://instagram.com/jokesshots" target="_blank" rel="noopener noreferrer">Instagram</a>
                <a href="#" class="js-email-link" data-i18n="footer.email">Email</a>
                <a href="../index.html#work" data-i18n="nav.work">Work</a>
            </div>
            <span class="footer-credit" data-i18n="footer.credit">Designed &amp; Developed by <a href="https://hi-one.de" target="_blank" rel="noopener noreferrer">Hi-One Media</a></span>
        </div>
    </footer>

    <div class="lightbox" id="lightbox">
        <button class="lightbox-close" id="lightboxClose" aria-label="Close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
        <div class="lightbox-counter" id="lightboxCounter"></div>
        <img class="lightbox-img" id="lightboxImg" src="" alt="">
        <button class="lightbox-prev" id="lightboxPrev" aria-label="Previous">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        <button class="lightbox-next" id="lightboxNext" aria-label="Next">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
    </div>

    <script src="../js/project.js"></script>
</body>
</html>
'''


def generate_gallery_item(page, wide=False):
    """Generate a single gallery grid item for index.html."""
    slug = page["slug"]
    title = page["title"]
    category = page["category"]
    label = CATEGORY_LABELS.get(category, category)
    titelbild = get_titelbild(page)
    if not titelbild:
        return ""

    wide_class = " gallery-item--wide" if wide else ""

    return f'''
                <a href="pages/{slug}.html" class="gallery-item{wide_class}" data-category="{category}" data-artist="{title}">
                    <div class="gallery-item-img">
                        <img src="assets/photos/medium/{slug}/{titelbild}" alt="{title}" loading="lazy">
                    </div>
                    <div class="gallery-item-logo">
                        <span class="gallery-logo-text">{title.upper()}</span>
                    </div>
                    <div class="gallery-item-info">
                        <span class="gallery-item-meta">{label}</span>
                    </div>
                </a>'''


def generate_marquee_names():
    """Generate marquee ticker content."""
    names = [p["title"] for p in PAGES]
    items = []
    for name in names:
        items.append(f"            <span>{name}</span>")
        items.append(f"            <span>&middot;</span>")
    # Duplicate for seamless scroll
    return "\n".join(items + items)


def generate_index_html():
    """Generate the gallery grid section and filter buttons for index.html."""
    # Gallery items — make some wide for visual interest
    wide_indices = {0, 5, 10, 14}  # Every few items gets wide treatment
    items = []
    for i, page in enumerate(PAGES):
        item = generate_gallery_item(page, wide=(i in wide_indices))
        if item:
            items.append(item)

    return "\n".join(items)


# ── Video Embed CSS ────────────────────────────────────────────────

VIDEO_CSS = '''
/* === VIDEO EMBEDS === */
.project-videos {
    padding: 40px 0;
    background: #fafafa;
}

.project-videos-heading {
    font-family: 'Lato', sans-serif;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 24px;
}

.video-embed-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
}

.video-embed-item {
    width: 100%;
}

.video-embed-wrap {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
    border-radius: 4px;
    background: #111;
}

.video-embed-wrap iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

.video-embed-title {
    margin-top: 8px;
    font-size: 13px;
    color: #777;
    font-weight: 400;
}

@media (min-width: 768px) {
    .video-embed-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1200px) {
    .video-embed-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
'''


# ── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("JOKESSHOTS Site Builder")
    print("=" * 50)

    # 1. Process photos
    process_photos()

    # 2. Delete old pages
    print("\n=== CLEANING OLD PAGES ===\n")
    old_pages = [
        "ice-cube.html", "burna-boy.html", "kaytranada.html", "larry-june.html",
        "boondawg.html", "soulside.html", "luciano.html", "og-keemo.html",
        "rin.html", "roddy-ricch.html", "westside-boogie.html", "misc.html"
    ]
    for p in old_pages:
        path = PAGES_DIR / p
        if path.exists():
            path.unlink()
            print(f"  Deleted: {p}")

    # 3. Generate new pages
    print("\n=== GENERATING PAGES ===\n")
    for i, page in enumerate(PAGES):
        next_page = PAGES[(i + 1) % len(PAGES)]
        html = generate_page_html(page, next_page)
        out_path = PAGES_DIR / f"{page['slug']}.html"
        out_path.write_text(html)
        photos = get_photos_for_page(page)
        videos = len(page.get("videos", []))
        print(f"  {page['slug']}.html — {len(photos)} photos, {videos} videos")

    # 4. Append video CSS to project.css
    print("\n=== ADDING VIDEO CSS ===\n")
    css_path = SRC / "css" / "project.css"
    css_content = css_path.read_text()
    if "video-embed" not in css_content:
        css_path.write_text(css_content + "\n" + VIDEO_CSS)
        print("  Added video embed styles to project.css")
    else:
        print("  Video embed styles already present")

    # 5. Generate gallery items for index.html reference
    print("\n=== GALLERY GRID (for index.html) ===\n")
    gallery_html = generate_index_html()
    marquee_html = generate_marquee_names()

    # Save as reference files
    (BASE / "gallery-items.html").write_text(gallery_html)
    (BASE / "marquee-items.html").write_text(marquee_html)
    print("  Saved gallery-items.html and marquee-items.html")
    print("  (These need to be inserted into index.html)")

    # 6. Summary
    print("\n=== SUMMARY ===\n")
    total_photos = sum(len(get_photos_for_page(p)) for p in PAGES)
    total_videos = sum(len(p.get("videos", [])) for p in PAGES)
    print(f"  Pages generated: {len(PAGES)}")
    print(f"  Total photos: {total_photos}")
    print(f"  Total video embeds: {total_videos}")
    print(f"  Filter categories: All / Concerts / Events / Portraits / Urban / Fashion")
    print("\n  Next: Insert gallery-items.html into index.html gallery grid")
    print("  Next: Insert marquee-items.html into index.html marquee")
    print("  Next: Update filter buttons in index.html")
    print("\nDone!")
