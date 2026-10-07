from flask import Flask, render_template, request, redirect, url_for
import os
import random
from datetime import datetime

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
ASSET_VERSION = "4"

GALLERY_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Masonry photo galleries, all rendered by templates/gallery.html.
# folder: IMAGE_FOLDERS key; section: page title suffix; sort: gallery_images()
# sort mode; natural_height: show images at their own aspect ratio, uncropped.
GALLERIES = {
    "illustration": {"folder": "illustration", "section": "Personal", "sort": "date_desc"},
    "portal": {"folder": "portal", "section": "Personal"},
    "street": {"folder": "street", "section": "Personal"},
    "superface": {"folder": "self", "section": "Personal"},
    "olympics": {"folder": "olympics", "section": "Design", "natural_height": True},
}

# Templates that live under templates/Projects/ instead of at the templates
# root, keyed by the short "finder" name used elsewhere in this file.
PROJECT_TEMPLATES = {
    "cs171": "Projects/cs171.html",
    "t4sg": "Projects/2ft.html",
    "commonspirit": "Projects/commonspirit.html",
}


def render_gallery(name):
    config = {"sort": "name", "natural_height": False, **GALLERIES[name]}
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

    return dict(img=img, gallery_images=gallery_images, asset_v=ASSET_VERSION)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        finder = request.form.get("finder", "").strip().lower()

        personal_websites = ["afvs", "essays", "fysemr", "gifafvs", "illustration", "portal", "street", "superface"]
        collab_websites = ["highlander", "recit", "olympics", "hackharvard", "merch"]
        flat = ["about", "collab", "cs171", "personal"]

        # ✅ If user types "t4sg" (or similar), send them to the t4sg page
        if finder in ["t4sg", "t4sg.html", "t4sg case study", "2feet", "t4sg x 2feet","2feet prosthetics", "tech 4 social good", "2ft"]:
            return render_template(PROJECT_TEMPLATES["t4sg"])

        if finder in ["commonspirit", "common spirit", "commonspirit health", "common spirit health", "t4sg x commonspirit"]:
            return render_template(PROJECT_TEMPLATES["commonspirit"])

        if finder in ["hack harvard", "hackharvard 2026", "hack to the moon", "hhuh"]:
            return render_template("collab websites/hackharvard.html")

        if finder in ["hpair", "hconf", "hudc", "cnn olympics", "stickers", "tote"]:
            return render_template("collab websites/merch.html")

        if finder in flat:
            return render_template(PROJECT_TEMPLATES.get(finder, f"{finder}.html"))
        elif finder in personal_websites:
            return render_sub_page(finder, "personal websites")
        elif finder in collab_websites:
            return render_sub_page(finder, "collab websites")

        elif finder in ["chi", "pirenily", "me", "chi le", "emily", "iron pig", "chi bell", "myself", "i", "artist"]:
            return render_template("about.html")
        elif finder in ["commission", "client work", "commissioned work", "commissions", "client",
                        "collaborative work", "collaborations", "collaboration", "member", "film",
                        "direction", "director", "collab", "graphic design", "clubs", "club", "design"]:
            return render_template("collab.html")
        elif finder in ["personal work", "self", "person", "mine", "free", "journey", "play"]:
            return render_template("personal.html")

        else:
            finder = random.choice(personal_websites + collab_websites + flat)
            if finder in personal_websites:
                return render_sub_page(finder, "personal websites")
            elif finder in collab_websites:
                return render_sub_page(finder, "collab websites")
            else:
                return render_template(PROJECT_TEMPLATES.get(finder, f"{finder}.html"))


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

@app.route("/client")
def client():
    return redirect(url_for("collab"))

@app.route("/personal")
def personal():
    return render_template("personal.html")

@app.route("/collab")
def collab():
    return render_template("collab.html")

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
