from flask import Flask, render_template, request, redirect, url_for
import difflib
import os
import random
import re
import struct
import subprocess
import unicodedata
from datetime import datetime
from functools import lru_cache

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-string"  # required for sessions

# Maps a stable logical name (used in templates) to the actual on-disk folder
# under static/asset/images/. Rename or move a folder on disk, update it here
# once, and every template that references it via img()/gallery_images()
# keeps working.
IMAGE_FOLDERS = {
    "about": "about",
    "afvs": "afvs",
    "design": "design",
    "art_direction": "art direction",
    "client": "client",
    "fish": "fish",
    "illustration": "illustration",
    "olympics": "client/olympics",
    "other": "other",
    "portal": "portal",
    "processing": "processing",
    "recit": "recit",
    "self": "self",
    "street": "street",
    "ux": "ux",
}

# Cache-busting version appended to local CSS/JS URLs (?v=...).
# Bump on every change so browsers fetch fresh assets.
ASSET_VERSION = "34"

GALLERY_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Photo galleries, all rendered by templates/gallery.html as justified rows.
# folder: IMAGE_FOLDERS key; section: page title suffix; sort: gallery_images()
# sort mode.
GALLERIES = {
    "illustration": {"folder": "illustration", "section": "Personal", "sort": "date_desc"},
    "portal": {"folder": "portal", "section": "Personal"},
    "street": {"folder": "street", "section": "Personal"},
    "superface": {"folder": "self", "section": "Personal"},
    "olympics": {"folder": "olympics", "section": "Design"},
}

# Templates that live under templates/Projects/ instead of at the templates
# root, keyed by the short "finder" name used elsewhere in this file.
PROJECT_TEMPLATES = {
    "cs171": "Projects/cs171.html",
    "t4sg": "Projects/2ft.html",
    "commonspirit": "Projects/commonspirit.html",
}


def render_gallery(name):
    config = {"sort": "name", **GALLERIES[name]}
    return render_template("gallery.html", **config)


def render_sub_page(name, folder):
    if name in GALLERIES:
        return render_gallery(name)
    return render_template(f"{folder}/{name}.html")


def _date_sort_key(filename):
    # illustration/ files are named D.M.YY(YY).ext; sort newest first.
    day, month, year = (int(p) for p in os.path.splitext(filename)[0].split("."))
    if year < 100:
        year += 2000
    return datetime(year, month, day)


@lru_cache(maxsize=None)
def _image_size(path):
    """(width, height) as displayed, read from the file header (no Pillow).
    JPEGs honour the EXIF orientation, like browsers do. None if unreadable."""
    try:
        with open(path, "rb") as f:
            data = f.read(256 * 1024)
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X":
            return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
        if chunk == b"VP8L":
            bits = int.from_bytes(data[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
        return None
    if data[:2] != b"\xff\xd8":
        return None
    i, rotated = 2, False
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        marker = data[i + 1]
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker == 0xE1 and data[i + 4:i + 10] == b"Exif\0\0":
            rotated = _exif_orientation(data[i + 10:i + 2 + length]) in (5, 6, 7, 8)
        elif 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (h, w) if rotated else (w, h)
        i += 2 + length
    return None


def _exif_orientation(tiff):
    end = "<" if tiff[:2] == b"II" else ">"
    try:
        ifd = struct.unpack(end + "I", tiff[4:8])[0]
        for n in range(struct.unpack(end + "H", tiff[ifd:ifd + 2])[0]):
            entry = ifd + 2 + 12 * n
            if struct.unpack(end + "H", tiff[entry:entry + 2])[0] == 0x0112:
                return struct.unpack(end + "H", tiff[entry + 8:entry + 10])[0]
    except struct.error:
        pass
    return 1


# Which top-nav item a page belongs to, so the nav can mark "you are here".
NAV_SECTIONS = {
    "about": ["about"],
    "design": ["design", "hackharvard", "merch", "olympics", "recit", "highlander"],
    "play": ["play", "afvs", "gifafvs", "essays", "fysemr", "illustration", "portal", "street", "superface"],
    "projects": ["t4sg", "commonspirit", "cs1710"],
}


def _last_updated():
    """'Oct 2026': date of the last commit, or of the newest file if git isn't around (e.g. on deploy)."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ct"], cwd=app.root_path,
                             capture_output=True, text=True, timeout=2).stdout.strip()
        stamp = int(out)
    except (OSError, ValueError, subprocess.SubprocessError):
        stamp = max(os.path.getmtime(os.path.join(d, f))
                    for root in (app.template_folder, app.static_folder)
                    for d, _, files in os.walk(os.path.join(app.root_path, root)) for f in files)
    return datetime.fromtimestamp(stamp).strftime("%b %Y")


LAST_UPDATED = _last_updated()

# Case studies in reading order; each one's footer links to the next (wrapping around).
CASE_STUDIES = [
    ("hackharvard", "HackHarvard 2026: Hack to the Moon"),
    ("merch", "Merch"),
    ("commonspirit", "T4SG × CommonSpirit Health"),
    ("cs171", "Chi x Rain: An Essay on Unicode"),
    ("t4sg", "T4SG × 2ft Prosthetics"),
]


@app.context_processor
def inject_site_info():
    endpoints = [e for e, _ in CASE_STUDIES]
    next_case = None
    if request.endpoint in endpoints:
        endpoint, title = CASE_STUDIES[(endpoints.index(request.endpoint) + 1) % len(CASE_STUDIES)]
        next_case = {"url": url_for(endpoint), "title": title}
    return dict(last_updated=LAST_UPDATED, next_case=next_case)


@app.context_processor
def inject_nav_section():
    page = request.path.strip("/").split("/")[0]
    section = next((name for name, pages in NAV_SECTIONS.items() if page in pages), None)
    return dict(nav_section=section)


@app.context_processor
def inject_image_helper():
    def img(folder, filename=""):
        real_folder = IMAGE_FOLDERS.get(folder, folder)
        path = f"asset/images/{real_folder}/{filename}".rstrip("/")
        return url_for("static", filename=path)

    def gallery_images(folder, sort="name"):
        real_folder = IMAGE_FOLDERS.get(folder, folder)
        dir_path = os.path.join(app.static_folder, "asset", "images", real_folder)
        if not os.path.isdir(dir_path):
            return []
        files = [
            f for f in os.listdir(dir_path)
            if os.path.splitext(f)[1].lower() in GALLERY_IMAGE_EXTENSIONS
        ]
        if sort == "date_desc":
            return sorted(files, key=_date_sort_key, reverse=True)
        return sorted(files)

    def image_ratio(folder, filename):
        """Width/height of a gallery image, for laying out justified rows."""
        real_folder = IMAGE_FOLDERS.get(folder, folder)
        size = _image_size(os.path.join(app.static_folder, "asset", "images", real_folder, filename))
        return round(size[0] / size[1], 4) if size and size[1] else 1.5

    def previews(folder, files=None, limit=8):
        """'|'-joined image URLs for a card's hover pop-ups (static/popups.js).
        Without files, takes a random handful from the folder's gallery."""
        if files is None:
            files = gallery_images(folder)
            files = random.sample(files, min(limit, len(files)))
        return "|".join(img(folder, f) for f in files)

    return dict(img=img, gallery_images=gallery_images, image_ratio=image_ratio, previews=previews, asset_v=ASSET_VERSION)

# Landing-page finder: every page and the words people might type to reach it.
# Matching is case-, accent- and punctuation-insensitive, so "Recít" == "recit".
SEARCH_INDEX = [
    ("/about", ["about", "about me", "chi", "chi le", "le tue chi", "tue", "chi tue le", "pirenily", "me",
                "myself", "emily", "iron pig", "chi bell", "artist", "bio", "contact", "email", "instagram",
                "linkedin", "github", "resume", "cv", "self photography"]),
    ("/design", ["design", "graphic design", "collab", "collaboration", "collaborations", "collaborative work",
                 "commission", "commissions", "commissioned work", "client", "client work", "clubs", "club",
                 "art direction", "art director", "director", "direction", "member", "logo", "logos", "poster",
                 "posters", "branding", "brand"]),
    ("/play", ["play", "personal", "personal work", "self", "mine", "free", "journey", "person", "fun"]),
    ("/#portfolio", ["projects", "project", "portfolio", "code", "coding projects", "ux", "ui", "uiux", "ui ux",
                     "case study", "case studies", "work", "cinenode", "cine node", "aerotone", "aero tone",
                     "arduino", "neural reconstruction", "handwritten curves", "handwriting", "machine learning"]),
    ("/hackharvard", ["hackharvard", "hack harvard", "hackharvard 2026", "hack to the moon", "hackathon",
                      "harvard hackathon", "hhuh", "director of design"]),
    ("/merch", ["merch", "merchandise", "hpair", "hconf", "aconf", "hudc", "the game", "harvard yale", "tote", "tote bag", "crest", "notebook",
                "stickers", "sticker", "pin", "t shirt", "shirt"]),
    ("/olympics", ["olympics", "cnn olympics", "olympic", "hoi thao", "cnn hoi thao", "team logos"]),
    ("/recit", ["recit", "recit film studio", "film studio", "hanoi"]),
    ("/highlander", ["highlander", "cnn english club", "english club", "cec", "cec oscar", "oscar", "short film",
                     "film", "matcha"]),
    ("https://www.facebook.com/official.ivmun", ["ivmun", "model un", "model united nations", "mun",
                                                 "vietnam model united nations", "conference"]),
    ("/afvs", ["afvs", "afvs 97", "coding and interactivity", "interactivity", "interactive", "p5", "p5js",
               "sketch", "pig", "a pigs death", "a pigs funeral", "pigs death", "pigs funeral", "sculpture",
               "projection", "360"]),
    ("/gifafvs", ["gifafvs", "what brings you here", "gif", "gifs"]),
    ("/essays", ["essays", "essay", "video essays", "video essay", "video"]),
    ("/fysemr", ["fysemr", "fysemr 65r", "tea garden", "land of rivers", "the land of rivers", "rivers",
                 "clip studio", "indesign"]),
    ("/superface", ["superface", "super face", "self portrait", "self portraits", "portrait", "portraits",
                    "makeup", "persona"]),
    ("/illustration", ["illustration", "illustrations", "drawing", "drawings", "cartoon", "cartoons", "art"]),
    ("/portal", ["portal", "the portal", "poems", "poem", "poetry", "short stories", "stories", "writing"]),
    ("/street", ["street", "street photography", "photography", "photos", "photo", "nikon", "camera"]),
    ("/t4sg", ["t4sg", "2ft", "2feet", "2 ft", "2 feet", "2ft prosthetics", "prosthetics", "t4sg x 2ft",
               "tech 4 social good", "tech for social good", "inventory"]),
    ("/commonspirit", ["commonspirit", "common spirit", "commonspirit health", "t4sg x commonspirit", "chna",
                       "health", "dashboard"]),
    ("/cs1710", ["cs171", "cs1710", "cs 171", "unicode", "chi x rain", "rain", "typos", "the typos",
                 "data visualization", "data vis", "dataviz", "visualization"]),
]


def _norm(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = text.replace("×", " x ").replace("'", "")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


_ALIASES = [(_norm(alias), url) for url, aliases in SEARCH_INDEX for alias in aliases]


def find_page(query):
    """Best page for a finder query, or None. Tried in order, most to least certain."""
    q = _norm(query)
    if not q:
        return None
    compact = q.replace(" ", "")

    # 1. Exact name, also ignoring spaces ("hack harvard" == "hackharvard")
    for alias, url in _ALIASES:
        if q == alias or compact == alias.replace(" ", ""):
            return url

    # 2. A known name inside a longer query ("show me street photography") — longest name wins
    hits = [(len(alias), url) for alias, url in _ALIASES
            if len(alias) >= 3 and re.search(rf"\b{re.escape(alias)}\b", q)]
    if hits:
        return max(hits)[1]

    # 3. Still typing: the query is the start of a name ("illus", "commonsp")
    if len(q) >= 3:
        hits = [(len(alias), url) for alias, url in _ALIASES
                if alias.startswith(q) or alias.replace(" ", "").startswith(compact)]
        if hits:
            return min(hits)[1]

    # 4. Typos: closest whole name, then closest single word
    names = {alias: url for alias, url in _ALIASES}
    close = difflib.get_close_matches(q, names, n=1, cutoff=0.78)
    if close:
        return names[close[0]]
    words = {}
    for alias, url in _ALIASES:
        for word in alias.split():
            if len(word) >= 4:
                words.setdefault(word, url)
    for token in sorted(q.split(), key=len, reverse=True):
        if len(token) >= 4:
            close = difflib.get_close_matches(token, words, n=1, cutoff=0.8)
            if close:
                return words[close[0]]
    return None


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    url = find_page(request.form.get("finder", ""))
    if url is None:
        # Nothing matched: keep the old surprise and open a random page
        url = random.choice([u for u, _ in SEARCH_INDEX if u.startswith("/") and u != "/#portfolio"])
    return redirect(url)


@app.route("/t4sg")
def t4sg():
    return render_template(PROJECT_TEMPLATES["t4sg"])


@app.route("/commonspirit")
def commonspirit():
    return render_template(PROJECT_TEMPLATES["commonspirit"])


# ---- your existing routes ----
@app.route("/about")
def about():
    return render_template("about.html")

# Old addresses still work: /collab and /client -> /design, /personal -> /play
@app.route("/collab")
@app.route("/client")
def collab():
    return redirect(url_for("design"), code=301)

@app.route("/personal")
def personal():
    return redirect(url_for("play"), code=301)

@app.route("/design")
def design():
    return render_template("collab.html")

@app.route("/play")
def play():
    return render_template("personal.html")

@app.route("/illustration")
def illustration():
    return render_gallery("illustration")

@app.route("/portal")
def portal():
    return render_gallery("portal")

@app.route("/street")
def street():
    return render_gallery("street")

@app.route("/superface")
def superface():
    return render_gallery("superface")

@app.route("/afvs")
def afvs():
    return render_template("personal websites/afvs.html")

@app.route("/gifafvs")
def gifafvs():
    return render_template("personal websites/gifafvs.html")

@app.route("/fysemr")
def fysemr():
    return render_template("personal websites/fysemr.html")

@app.route("/essays")
def essays():
    return render_template("personal websites/essays.html")

@app.route("/highlander")
def highlander():
    return render_template("collab websites/highlander.html")

@app.route("/recit")
def recit():
    return render_template("collab websites/recit.html")

@app.route("/olympics")
def olympics():
    return render_gallery("olympics")

@app.route("/hackharvard")
def hackharvard():
    return render_template("collab websites/hackharvard.html")

@app.route("/merch")
def merch():
    return render_template("collab websites/merch.html")

@app.route("/cs1710")
def cs171():
    return render_template(PROJECT_TEMPLATES["cs171"])

if __name__ == "__main__":
    app.run(debug=True)
