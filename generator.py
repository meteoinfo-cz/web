 import os

import json

import re

import random

import shutil


MOJE_DOMENA = "https://www.meteoinfo.cz"


def vytvor_slug(text):

    text = text.lower()

    mapa = {'á':'a', 'č':'c', 'ď':'d', 'é':'e', 'ě':'e', 'í':'i', 'ň':'n', 'ó':'o', 'ř':'r', 'š':'s', 'ť':'t', 'ú':'u', 'ů':'u', 'ý':'y', 'ž':'z'}

    for znak, nahrada in mapa.items():

        text = text.replace(znak, nahrada)

    text = re.sub(r'[^a-z0-9\s-]', '', text)

    return re.sub(r'[\s-]+', '-', text).strip('-')


sablona_cesta = 'sablona.html'

vystup_cesta = 'web'


with open(sablona_cesta, 'r', encoding='utf-8') as f:

    puvodni_kod = f.read()


vzor = r'\{\s*"n"\s*:\s*"([^"]+)"\s*,\s*"la"\s*:\s*([0-9.]+)\s*,\s*"lo"\s*:\s*([0-9.]+)'

nalezena_mesta = re.findall(vzor, puvodni_kod)


sitemap_odkazy = [f"  <url>\n    <loc>{MOJE_DOMENA}/</loc>\n    <priority>1.00</priority>\n  </url>"]

mesta_pro_json = []


for m_jmeno, m_lat, m_lon in nalezena_mesta:

    m_slug = vytvor_slug(m_jmeno)

    sitemap_odkazy.append(f"  <url>\n    <loc>{MOJE_DOMENA}/{m_slug}/</loc>\n    <priority>0.80</priority>\n  </url>")

    

    mesto_slozky_cesta = os.path.join(vystup_cesta, m_slug)

    os.makedirs(mesto_slozky_cesta, exist_ok=True)

    

    upraveny_html = puvodni_kod.replace('{{MESTO_TITUL}}', f' pro {m_jmeno}')

    upraveny_html = upraveny_html.replace('{{MESTO}}', m_jmeno)

    upraveny_html = upraveny_html.replace('{{MESTO_URL}}', m_slug)

    

    with open(os.path.join(mesto_slozky_cesta, 'index.html'), 'w', encoding='utf-8') as f:

        f.write(upraveny_html)


    mesta_pro_json.append({

        "n": m_jmeno, "la": float(m_lat), "lo": float(m_lon),

        "t": 20.0, "v": 10.0, "p": 1013, "s": 0.0, "sn": 0.0, "uv": 2

    })


os.makedirs(vystup_cesta, exist_ok=True)


with open(os.path.join(vystup_cesta, 'mesta.json'), 'w', encoding='utf-8') as f:

    json.dump(mesta_pro_json, f, ensure_ascii=False)


sitemap_vysledek = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

sitemap_vysledek += "\n".join(sitemap_odkazy) + "\n</urlset>"


sitemap_cesta_fin = os.path.join(vystup_cesta, 'sitemap.xml')

with open(sitemap_cesta_fin, 'w', encoding='utf-8') as f:

    f.write(sitemap_vysledek)


print("HOTOVO ULOŽENO!")

zde je generator py