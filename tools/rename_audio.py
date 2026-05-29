# -*- coding: utf-8 -*-
"""
Copy the Unit 1 audio files into the website, renamed to clean web-safe names.
NON-DESTRUCTIVE: your original files are left exactly as they are; renamed COPIES
are written into the destination folder.

Usage:
    python3 rename_audio.py "<source folder with your 100 mp3s>" "<destination, e.g. site/audio/unit1>"

It matches your files even if the names use spaces, underscores, apostrophes,
or different capitalisation.
"""
import sys, os, re, shutil, unicodedata

MAPPING = [
    {
        "from": "Aisha al-Bauniyya.mp3",
        "to": "aisha-al-bauniyya.mp3"
    },
    {
        "from": "Abbasid Caliphate.mp3",
        "to": "abbasid-caliphate.mp3"
    },
    {
        "from": "the Analects.mp3",
        "to": "the-analects.mp3"
    },
    {
        "from": "ancestor veneration.mp3",
        "to": "ancestor-veneration.mp3"
    },
    {
        "from": "artisans.mp3",
        "to": "artisans.mp3"
    },
    {
        "from": "Ashoka.mp3",
        "to": "ashoka.mp3"
    },
    {
        "from": "Bantu migrations.mp3",
        "to": "bantu-migrations.mp3"
    },
    {
        "from": "Bhakti movement.mp3",
        "to": "bhakti-movement.mp3"
    },
    {
        "from": "Brahmin.mp3",
        "to": "brahmin.mp3"
    },
    {
        "from": "caste system.mp3",
        "to": "caste-system.mp3"
    },
    {
        "from": "Champa rice.mp3",
        "to": "champa-rice.mp3"
    },
    {
        "from": "Chan Buddhism.mp3",
        "to": "chan-buddhism.mp3"
    },
    {
        "from": "Chang'an.mp3",
        "to": "chang-an.mp3"
    },
    {
        "from": "civil service exam.mp3",
        "to": "civil-service-exam.mp3"
    },
    {
        "from": "Chola dynasty.mp3",
        "to": "chola-dynasty.mp3"
    },
    {
        "from": "Confucianism.mp3",
        "to": "confucianism.mp3"
    },
    {
        "from": "Corvee labor.mp3",
        "to": "corvee-labor.mp3"
    },
    {
        "from": "Crusades.mp3",
        "to": "crusades.mp3"
    },
    {
        "from": "Daoism.mp3",
        "to": "daoism.mp3"
    },
    {
        "from": "Delhi Sultanate.mp3",
        "to": "delhi-sultanate.mp3"
    },
    {
        "from": "Dharma.mp3",
        "to": "dharma.mp3"
    },
    {
        "from": "Diaspora.mp3",
        "to": "diaspora.mp3"
    },
    {
        "from": "Eightfold Path.mp3",
        "to": "eightfold-path.mp3"
    },
    {
        "from": "Ethiopia.mp3",
        "to": "ethiopia.mp3"
    },
    {
        "from": "Feudalism.mp3",
        "to": "feudalism.mp3"
    },
    {
        "from": "Filial piety.mp3",
        "to": "filial-piety.mp3"
    },
    {
        "from": "Forbidden City.mp3",
        "to": "forbidden-city.mp3"
    },
    {
        "from": "Four Noble Truths.mp3",
        "to": "four-noble-truths.mp3"
    },
    {
        "from": "Grand Canal.mp3",
        "to": "grand-canal.mp3"
    },
    {
        "from": "Great Wall.mp3",
        "to": "great-wall.mp3"
    },
    {
        "from": "Great Zimbabwe.mp3",
        "to": "great-zimbabwe.mp3"
    },
    {
        "from": "Gupta Empire.mp3",
        "to": "gupta-empire.mp3"
    },
    {
        "from": "Han Dynasty.mp3",
        "to": "han-dynasty.mp3"
    },
    {
        "from": "Hausa Kingdoms.mp3",
        "to": "hausa-kingdoms.mp3"
    },
    {
        "from": "Hebrew Bible.mp3",
        "to": "hebrew-bible.mp3"
    },
    {
        "from": "Heian period.mp3",
        "to": "heian-period.mp3"
    },
    {
        "from": "House of Wisdom.mp3",
        "to": "house-of-wisdom.mp3"
    },
    {
        "from": "Imperial bureaucracy.mp3",
        "to": "imperial-bureaucracy.mp3"
    },
    {
        "from": "Inca Empire.mp3",
        "to": "inca-empire.mp3"
    },
    {
        "from": "Indian Ocean Maritime System.mp3",
        "to": "indian-ocean-maritime-system.mp3"
    },
    {
        "from": "Jati.mp3",
        "to": "jati.mp3"
    },
    {
        "from": "Judaism.mp3",
        "to": "judaism.mp3"
    },
    {
        "from": "Karma.mp3",
        "to": "karma.mp3"
    },
    {
        "from": "Kowtow.mp3",
        "to": "kowtow.mp3"
    },
    {
        "from": "Laozi.mp3",
        "to": "laozi.mp3"
    },
    {
        "from": "Legalism.mp3",
        "to": "legalism.mp3"
    },
    {
        "from": "Mahayana Buddhism.mp3",
        "to": "mahayana-buddhism.mp3"
    },
    {
        "from": "Majapahit Kingdom.mp3",
        "to": "majapahit-kingdom.mp3"
    },
    {
        "from": "Mali.mp3",
        "to": "mali.mp3"
    },
    {
        "from": "Mamluks.mp3",
        "to": "mamluks.mp3"
    },
    {
        "from": "Mauryan Empire.mp3",
        "to": "mauryan-empire.mp3"
    },
    {
        "from": "Mayans.mp3",
        "to": "mayans.mp3"
    },
    {
        "from": "Meritocracy.mp3",
        "to": "meritocracy.mp3"
    },
    {
        "from": "Mesa Verde.mp3",
        "to": "mesa-verde.mp3"
    },
    {
        "from": "Moche.mp3",
        "to": "moche.mp3"
    },
    {
        "from": "Moksha.mp3",
        "to": "moksha.mp3"
    },
    {
        "from": "Monarchies.mp3",
        "to": "monarchies.mp3"
    },
    {
        "from": "Monastic living.mp3",
        "to": "monastic-living.mp3"
    },
    {
        "from": "Monsoons.mp3",
        "to": "monsoons.mp3"
    },
    {
        "from": "Mudras.mp3",
        "to": "mudras.mp3"
    },
    {
        "from": "Nasir al-Din al-Tusi.mp3",
        "to": "nasir-al-din-al-tusi.mp3"
    },
    {
        "from": "Nirvana.mp3",
        "to": "nirvana.mp3"
    },
    {
        "from": "Neo-Confucianism.mp3",
        "to": "neo-confucianism.mp3"
    },
    {
        "from": "Oligarchy.mp3",
        "to": "oligarchy.mp3"
    },
    {
        "from": "Olmec.mp3",
        "to": "olmec.mp3"
    },
    {
        "from": "Parthians.mp3",
        "to": "parthians.mp3"
    },
    {
        "from": "Pataliputra.mp3",
        "to": "pataliputra.mp3"
    },
    {
        "from": "Patriarchy.mp3",
        "to": "patriarchy.mp3"
    },
    {
        "from": "Polygyny.mp3",
        "to": "polygyny.mp3"
    },
    {
        "from": "Proto-industrialization.mp3",
        "to": "proto-industrialization.mp3"
    },
    {
        "from": "Qin Dynasty.mp3",
        "to": "qin-dynasty.mp3"
    },
    {
        "from": "Rajput Kingdoms.mp3",
        "to": "rajput-kingdoms.mp3"
    },
    {
        "from": "Reciprocity.mp3",
        "to": "reciprocity.mp3"
    },
    {
        "from": "Reincarnation.mp3",
        "to": "reincarnation.mp3"
    },
    {
        "from": "Sanskrit.mp3",
        "to": "sanskrit.mp3"
    },
    {
        "from": "Scholar Gentry.mp3",
        "to": "scholar-gentry.mp3"
    },
    {
        "from": "Shinto.mp3",
        "to": "shinto.mp3"
    },
    {
        "from": "Shiva.mp3",
        "to": "shiva.mp3"
    },
    {
        "from": "Sinhala dynasties.mp3",
        "to": "sinhala-dynasties.mp3"
    },
    {
        "from": "Silk Road.mp3",
        "to": "silk-road.mp3"
    },
    {
        "from": "Song Dynasty.mp3",
        "to": "song-dynasty.mp3"
    },
    {
        "from": "Srivijaya Empire.mp3",
        "to": "srivijaya-empire.mp3"
    },
    {
        "from": "Sufis.mp3",
        "to": "sufis.mp3"
    },
    {
        "from": "Sukhothai Kingdom.mp3",
        "to": "sukhothai-kingdom.mp3"
    },
    {
        "from": "Swahili.mp3",
        "to": "swahili.mp3"
    },
    {
        "from": "Syncretism.mp3",
        "to": "syncretism.mp3"
    },
    {
        "from": "Tang Dynasty.mp3",
        "to": "tang-dynasty.mp3"
    },
    {
        "from": "Teotihuacan.mp3",
        "to": "teotihuacan.mp3"
    },
    {
        "from": "Theater State.mp3",
        "to": "theater-state.mp3"
    },
    {
        "from": "Theravada Buddhism.mp3",
        "to": "theravada-buddhism.mp3"
    },
    {
        "from": "Tibetan Buddhism.mp3",
        "to": "tibetan-buddhism.mp3"
    },
    {
        "from": "Trans-Saharan Trade Routes.mp3",
        "to": "trans-saharan-trade-routes.mp3"
    },
    {
        "from": "Universalizing Religion.mp3",
        "to": "universalizing-religion.mp3"
    },
    {
        "from": "Urdu.mp3",
        "to": "urdu.mp3"
    },
    {
        "from": "Varna.mp3",
        "to": "varna.mp3"
    },
    {
        "from": "Vedas.mp3",
        "to": "vedas.mp3"
    },
    {
        "from": "Vijayanagara Empire.mp3",
        "to": "vijayanagara-empire.mp3"
    },
    {
        "from": "Vishnu.mp3",
        "to": "vishnu.mp3"
    },
    {
        "from": "Woodblock printing.mp3",
        "to": "woodblock-printing.mp3"
    },
    {
        "from": "Xiongnu.mp3",
        "to": "xiongnu.mp3"
    }
]  # list of {"from": original.mp3, "to": slug.mp3}

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", s.lower())

def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    have = {}
    for f in os.listdir(src):
        if f.lower().endswith(".mp3"):
            have[norm(os.path.splitext(f)[0])] = f
    copied, missing = 0, []
    for m in MAPPING:
        key = norm(os.path.splitext(m["from"])[0])
        if key in have:
            shutil.copyfile(os.path.join(src, have[key]), os.path.join(dst, m["to"]))
            copied += 1
        else:
            missing.append(m["from"])
    print("Copied %d of %d files into %s" % (copied, len(MAPPING), dst))
    if missing:
        print("\nCould NOT find matches for these (check the source folder):")
        for x in missing: print("  -", x)
    else:
        print("All 100 files matched and copied. You're ready to commit.")

if __name__ == "__main__":
    main()
