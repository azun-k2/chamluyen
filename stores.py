#!/usr/bin/env python3
"""Writes the three store cards of download.html (English root and vi/) from the `live` flags of Chăm luyện in
../_tools/site-family/family.json, the same flags `site-family.py check` keeps up to date. Run after
`../_tools/site-family.py check`; with `--new` it also creates the two pages from support.html (once).
A store that is not live shows its greyed badge and "Sắp ra mắt" (no link); a live one links to the store."""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILY = json.loads((HERE.parent / "_tools/site-family/family.json").read_text())
APP = next(a for a in FAMILY["apps"] if a["slug"] == "chamluyen")

TEXT = {
    "vi": {"title": "Tải ứng dụng", "soon": "Sắp ra mắt", "badge": {"ios": "ios-vi.svg", "android": "play-vi.png", "mac": "mac-vi.svg"},
           "label": {"ios": "Tải ứng dụng cho iPhone/iPad trên App Store",
                     "android": "Tải ứng dụng cho Android/Tablet (Samsung/Xiaomi/OPPO v.v.) trên Google Play",
                     "mac": "Tải ứng dụng cho máy Mac trên Mac App Store"},
           "alt": {"ios": "Tải về trên App Store", "android": "Tải nội dung trên Google Play", "mac": "Tải về trên Mac App Store"},
           "intro": "Chọn cửa hàng ứng dụng phù hợp với thiết bị của bé.",
           "desc": "Tải Chăm luyện cho iPhone, iPad, Android, máy tính bảng và Mac.", "up": "../"},
    "en": {"title": "Get the app", "soon": "Coming soon", "badge": {"ios": "download-on-the-app-store.svg", "android": "google-play-badge.png", "mac": "download-on-the-mac-app-store.svg"},
           "label": {"ios": "Get the app for iPhone and iPad on the App Store",
                     "android": "Get the app for Android phones and tablets (Samsung, Xiaomi, OPPO and others) on Google Play",
                     "mac": "Get the app for Mac on the Mac App Store"},
           "alt": {"ios": "Download on the App Store", "android": "Get it on Google Play", "mac": "Download on the Mac App Store"},
           "intro": "Pick the store that matches your child's device.",
           "desc": "Get Chăm luyện for iPhone, iPad, Android phones and tablets, and Mac.", "up": ""},
}
URL = {"ios": f"https://apps.apple.com/app/id{APP['appStoreId']}?platform=iphone",
       "mac": f"https://apps.apple.com/app/id{APP['appStoreId']}?platform=mac",
       "android": f"https://play.google.com/store/apps/details?id={APP['playId']}"}
ORDER = ("ios", "android", "mac")


def cards(lang):
    t = TEXT[lang]; out = []
    for st in ORDER:
        src = f'{t["up"]}family/badges/{t["badge"][st]}'
        if APP["live"].get(st):
            badge = f'<a class="family-store" href="{URL[st]}"><img src="{src}" alt="{t["alt"][st]}" height="46"></a>'
        else:
            badge = (f'<span class="family-store soon" title="{t["soon"]}"><img src="{src}" alt="{t["alt"][st]}: {t["soon"]}" height="46">'
                     f'<span class="family-soon">{t["soon"]}</span></span>')
        out.append(f'  <div class="get-item">\n    <h3>{t["label"][st]}</h3>\n    {badge}\n  </div>')
    return "\n".join(out)


def block(lang):
    t = TEXT[lang]
    return (f'<!-- chamluyen:stores -->\n<section class="card">\n  <h2>{t["title"]}</h2>\n  <p>{t["intro"]}</p>\n{cards(lang)}\n</section>\n<!-- /chamluyen:stores -->')


def create(lang):
    src = (HERE / ("vi/support.html" if lang == "vi" else "support.html")).read_text()
    t = TEXT[lang]
    a, b = src.index('<section class="card">'), src.index("<footer>")
    page = src[:a] + block(lang) + "\n" + src[b:]
    page = re.sub(r"<script src=\"[^\"]*contact\.js\"[^>]*></script>\n?", "", page)
    page = re.sub(r'<p class="tagline">.*?</p>', f'<p class="tagline">{t["title"]}</p>', page, count=1)
    page = re.sub(r"<title>.*?</title>", f"<title>Chăm luyện — {t['title'].lower()}</title>", page, count=1)
    page = re.sub(r'(name="description" content=")[^"]*', rf"\g<1>{t['desc']}", page)
    page = re.sub(r'(property="og:(?:title)" content=")[^"]*', rf"\g<1>Chăm luyện — {t['title'].lower()}", page)
    page = re.sub(r'(property="og:description" content=")[^"]*', rf"\g<1>{t['desc']}", page)
    page = page.replace("support.html", "download.html")
    return page


def main():
    for lang, path in (("vi", HERE / "vi/download.html"), ("en", HERE / "download.html")):
        if "--new" in sys.argv and not path.exists():
            path.write_text(create(lang)); print("created", path.name, lang)
        text = path.read_text()
        text = re.sub(r"<!-- chamluyen:stores -->.*?<!-- /chamluyen:stores -->", lambda m: block(lang), text, flags=re.S)
        path.write_text(text); print("stores written", path.relative_to(HERE))


if __name__ == "__main__":
    main()
