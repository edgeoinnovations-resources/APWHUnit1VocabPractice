# -*- coding: utf-8 -*-
"""Builds the Unit 1 data files and the audio rename helper from a single source of truth."""
import json, re, unicodedata, os

CONCEPTS = {
    "rel":    "Religions & Belief Systems",
    "gov":    "Government & Political Organization",
    "soc":    "Social Structure & Hierarchy",
    "econ":   "Economy, Trade & Technology",
    "states": "States & Empires",
    "people": "People & Key Figures",
}
REGIONS = {
    "eastasia": "East Asia",
    "islam":    "Dar al-Islam",
    "ssasia":   "South & Southeast Asia",
    "americas": "The Americas",
    "africa":   "Africa",
    "europe":   "Europe",
}

# (term, definition, [concepts], region|None, audio_filename_from_manifest)
R = [
("\u2018A\u2019ishah al-Ba\u2019uniyyah", "most prolific female Muslim writer and poet before the 20th century", ["people","rel"], "islam", "Aisha al-Bauniyya"),
("Abbasid Caliphate", "dynasty of the Muslim empire of the caliphate that followed the Umayyad Caliphate; destroyed by the Mongol invasion in 1258", ["states","gov"], "islam", "Abbasid Caliphate"),
("The Analects", "the compilation of Confucius\u2019 teachings after his death", ["rel"], "eastasia", "the Analects"),
("Ancestor Veneration", "a Confucian practice of praying to one's ancestors", ["rel","soc"], "eastasia", "ancestor veneration"),
("Artisans", "skilled manual workers in a particular craft who often work by hand", ["econ","soc"], None, "artisans"),
("Ashoka", "the third king of the Mauryan Empire who promoted Buddhism", ["people","gov"], "ssasia", "Ashoka"),
("Bantu Migrations", "the spread of Bantu-speaking peoples from their homeland in what is now southern Nigeria to most of Africa", ["soc"], "africa", "Bantu migrations"),
("Bhakti Movement", "Hindu devotional movement that flourished in the early modern era, emphasizing music, dance, poetry, and rituals as means by which to achieve direct union with the divine", ["rel"], "ssasia", "Bhakti movement"),
("Brahman", "Hindu spirit that is the energy that connects everything; a priest class", ["rel","soc"], "ssasia", "Brahmin"),
("Caste System", "a rigid social system in India that gives every Indian a particular place in the social hierarchy from birth", ["soc"], "ssasia", "caste system"),
("Champa Rice", "an Indian quick-maturing, very resistant rice that could be harvested twice in one growing season", ["econ"], "eastasia", "Champa rice"),
("Chan Buddhism", "a Chinese school of Mah\u0101y\u0101na Buddhism popular during the Tang and Song Dynasties", ["rel"], "eastasia", "Chan Buddhism"),
("Chang\u2019an", "ancient Chinese capital of several dynasties; now known as Xi\u2019an", ["gov","econ"], "eastasia", "Chang'an"),
("Civil Service Exam", "a system of testing designed to select the most studious and learned candidates for appointment as bureaucrats in the Chinese government", ["gov"], "eastasia", "civil service exam"),
("Chola Dynasty", "a Tamil maritime empire of southern India and one of the longest-ruling dynasties in world history", ["states"], "ssasia", "Chola dynasty"),
("Confucianism", "the system of ethics, education, and statesmanship taught by Confucius and his disciples, stressing love for humanity, ancestor worship, reverence for parents, and harmony in thought and conduct", ["rel"], "eastasia", "Confucianism"),
("Corvee Labor", "forced, unpaid labor that was often intermittent", ["econ","soc"], None, "Corvee labor"),
("Crusades", "a series of Christian holy wars conducted against nonbelievers", ["rel"], "europe", "Crusades"),
("Daoism", "a Chinese philosophy based on the teachings of Lao Zi which taught that people should turn to nature and give up their worldly concerns; was largely a spiritual alternative to Confucianism", ["rel"], "eastasia", "Daoism"),
("Delhi Sultanate", "a Muslim kingdom that ruled parts of India from the 13th to the 16th centuries and was an Islamic state on the outside of the Caliphate system", ["states"], "ssasia", "Delhi Sultanate"),
("Dharma", "a position and career determined by birth within the caste system", ["rel","soc"], "ssasia", "Dharma"),
("Diaspora", "any movement of the citizens of a population sharing the same ethnic descent", ["soc"], None, "Diaspora"),
("Eightfold Path", "one of Buddha\u2019s teachings which outlines the path to nirvana", ["rel"], None, "Eightfold Path"),
("Ethiopia", "Christian-led African kingdom that emerged in the 12th century; known for their rock hewn churches", ["states","rel"], "africa", "Ethiopia"),
("Feudalism", "a land system in which a king owned all the land a granted tracks to nobles in exchange for military loyalty, and nobles granted parts of their land to vassals or serfs who worked the land", ["gov","econ"], None, "Feudalism"),
("Filial Piety", "a Confucian virtue of respect, obedience, and care for one's parents and elderly family members", ["rel","soc"], "eastasia", "Filial piety"),
("Forbidden City", "a walled section of Beijing built in the Ming Dynasty where emperors lived between 1121 and 1911", ["gov"], "eastasia", "Forbidden City"),
("Four Noble Truths", "Buddha\u2019s guiding principles regarding suffering", ["rel"], None, "Four Noble Truths"),
("Grand Canal", "an over 1,000 mile-long transportation waterway that allowed China to be the most populous trading area in the world during the Song Dynasty", ["econ"], "eastasia", "Grand Canal"),
("Great Wall", "a Chinese defensive fortification built during the reign of Shi Huangdi to keep out northern nomadic invaders", ["gov"], "eastasia", "Great Wall"),
("Great Zimbabwe", "a powerful state in the African interior that emerged from the growing trade in gold to the East African coast", ["states","econ"], "africa", "Great Zimbabwe"),
("Gupta Empire", "the empire that later united India following the Maurya Empire", ["states"], "ssasia", "Gupta Empire"),
("Han Dynasty", "China\u2019s longest running dynasty", ["states"], "eastasia", "Han Dynasty"),
("Hausa Kingdoms", "a group of small independent city-states in northern central Africa", ["states"], "africa", "Hausa Kingdoms"),
("Hebrew Bible", "collection of sacred books containing diverse materials concerning the origins, experiences, beliefs and practices of the Israelites", ["rel"], None, "Hebrew Bible"),
("Heian Period", "a period when Japan was most closely connected to and influenced by Chinese culture that lasted lasted from 794 to 1185 CE", ["states"], "eastasia", "Heian period"),
("House of Wisdom", "an academic center for research and translation of foreign texts that was established in Baghdad by the Abbasid caliph al-Mamun", ["econ","gov"], "islam", "House of Wisdom"),
("Imperial Bureaucracy", "large organization in China in which appointed officials carried out the policies of the empire", ["gov"], "eastasia", "Imperial bureaucracy"),
("Inca Empire", "largest imperial state in the Americas in the 15th and 16th centuries. The empire spanned almost the entire coast of western South America", ["states"], "americas", "Inca Empire"),
("Indian Ocean Maritime System", "a trade route across the Indian Ocean and the South China Sea", ["econ"], None, "Indian Ocean Maritime System"),
("Jati", "a classification within the Indian caste system", ["soc"], "ssasia", "Jati"),
("Judaism", "oldest known monotheistic religion", ["rel"], None, "Judaism"),
("Karma", "the effects of a person's actions that determine his destiny in his next incarnation", ["rel"], None, "Karma"),
("Kowtow", "an act of deep respect shown by kneeling and bowing so low as to have one's head touching the ground", ["soc","gov"], "eastasia", "Kowtow"),
("Lao Zi", "a Chinese philosopher who taught retreat from society into nature and that individuals should seek to become attuned with Dao", ["people","rel"], "eastasia", "Laozi"),
("Legalism", "a political philosophy in China that emphasized the unruliness of human nature and justified state coercion and control. The Qin rulers and early Han rulers invoked it to validate the authoritarian nature of their regimes", ["gov","rel"], "eastasia", "Legalism"),
("Mahayana Buddhism", "focuses on service and became popular in China and Korea", ["rel"], "eastasia", "Mahayana Buddhism"),
("Majapahit Kingdom", "Buddhist Kingdom from 1293-1520 based on Java that gained power by controlling sea routes", ["states"], "ssasia", "Majapahit Kingdom"),
("Mali", "trading empire that flourished in western Africa from the 13th to the 16th century and was known for its wealth", ["states","econ"], "africa", "Mali"),
("Mamluks", "enslaved soldiers from the Abbasid era", ["soc","gov"], "islam", "Mamluks"),
("Mauryan Empire", "it unified most of India into a peaceful and stable empire and expanded trade", ["states"], "ssasia", "Mauryan Empire"),
("Mayans", "established a series of independent states and city-states in Mesoamerica", ["states"], "americas", "Mayans"),
("Meritocracy", "the exam system that granted Chinese officials their positions", ["gov"], "eastasia", "Meritocracy"),
("Mesa Verde", "the largest complex of Anasazi cliff-dwellings in the United States Southwest", ["states"], "americas", "Mesa Verde"),
("Moche", "a civilization near the coast of Peru that built irrigation networks and urban centers that had brick temples", ["states"], "americas", "Moche"),
("Moksha", "the goal for Hindus in which you are reunited with Brahman and escape reincarnation", ["rel"], None, "Moksha"),
("Monarchies", "governments in which the supreme power is lodged in the hands of a monarch who reigns over a state or territory, usually for life and by hereditary right", ["gov"], None, "Monarchies"),
("Monastic Living", "a religious way of life in which one renounces worldly pursuits to devote oneself fully to spiritual work", ["rel"], None, "Monastic living"),
("Monsoons", "a seasonal wind of the Indian Ocean and southern Asia which affected trade routes", ["econ"], None, "Monsoons"),
("Mudras", "a hand gesture with specific meaning or significance in Indian classical sculpture and dance", ["rel","soc"], "ssasia", "Mudras"),
("Nasir al-Din al-Tusi", "Persian mathematician; one of the most celebrated Islamic scholars", ["people"], "islam", "Nasir al-Din al-Tusi"),
("Nirvana", "the state of liberation from suffering which can be achieved when an individual follows the Eightfold Path in Buddhism", ["rel"], None, "Nirvana"),
("Neo-Confucianism", "the revival of Confucian teachings during the Tang and Song dynasties and a subsequent synthesis of Confucianism with aspects of Buddhism and Daoism", ["rel"], "eastasia", "Neo-Confucianism"),
("Oligarchy", "form of government in which a small group of elites make decisions for everyone", ["gov"], None, "Oligarchy"),
("Olmec", "the earliest known Mexican civilizations", ["states"], "americas", "Olmec"),
("Parthians", "Persian dynasty based in Iran that extended into Mesopotamia", ["states"], "islam", "Parthians"),
("Pataliputra", "the chief political and commercial center of northern India", ["gov","econ"], "ssasia", "Pataliputra"),
("Patriarchy", "society in which men hold power within the family, in governance, and/or in economics", ["soc"], None, "Patriarchy"),
("Polygyny", "a form of polygamy in which a man has two or more wives simultaneously", ["soc"], None, "Polygyny"),
("Proto-industrialization", "people in rural areas producing more goods than they can sell", ["econ"], None, "Proto-industrialization"),
("Qin Dynasty", "the Chinese dynasty that established the first centralized imperial government and built much of the Great Wall, Replaced the Zhou dynasty and employed legalist ideas in order to control warring states and unify the country", ["states"], "eastasia", "Qin Dynasty"),
("Rajput Kingdoms", "Hindu kingdoms that arose after the fall of the Gupta Empire", ["states"], "ssasia", "Rajput Kingdoms"),
("Reciprocity", "a relationship between people and state where people pay tribute in exchange for access to resources", ["econ","gov"], None, "Reciprocity"),
("Reincarnation", "Hindu principle in which souls pass to other beings after death", ["rel"], None, "Reincarnation"),
("Sanskrit", "sacred language of the Vedas in India", ["rel","soc"], "ssasia", "Sanskrit"),
("Scholar Gentry", "Confucian educated social class that became the most influential social class of China", ["soc"], "eastasia", "Scholar Gentry"),
("Shinto", "the indigenous religion of Japan in which people believed that kami (spirits) were present in their natural surroundings", ["rel"], "eastasia", "Shinto"),
("Shiva", "an important Hindu deity who in the trinity of gods was the Destroyer", ["rel"], "ssasia", "Shiva"),
("Sinhala Dynasties", "Sri Lankan dynasties which were largely Buddhist", ["states"], "ssasia", "Sinhala dynasties"),
("Silk Road", "a vast network of trading routes that connected the East to the West: Constantinople in Europe to Chang'an in Asia", ["econ"], None, "Silk Road"),
("Song Dynasty", "a Chinese imperial dynasty that ruled from 960 to 1279 that preceded the Yuan Dynasty", ["states"], "eastasia", "Song Dynasty"),
("Srivijaya Empire", "an Indonesian Hindu sea-based empire based on the island of Sumatra, Indonesia which was an important trade center", ["states"], "ssasia", "Srivijaya Empire"),
("Sufis", "a mystical Muslim group that had successful missionaries. They believed they could become closer to God through prayer, fasting, and a simple life", ["rel"], "islam", "Sufis"),
("Sukhothai Kingdom", "a kingdom in north central Thailand from 1238 until 1438", ["states"], "ssasia", "Sukhothai Kingdom"),
("Swahili", "blended language that combined Bantu and Arabic languages and is still spoken today", ["soc"], "africa", "Swahili"),
("Syncretism", "the blending of elements from more than one religion into a distinct system of worship", ["rel"], None, "Syncretism"),
("Tang Dynasty", "Chinese imperial dynasty which preceded the Song; one of the greatest periods of peace and prosperity in Chinese history, and it is remembered for its cultural achievements and its strong centralized government", ["states"], "eastasia", "Tang Dynasty"),
("Teotihuacan", "a major city in Mesoamerica that was the center for cultural and religious activities", ["states","rel"], "americas", "Teotihuacan"),
("Theater State", "a state that acquires prestige and power by developing attractive cultural forms and staging elaborate public ceremonies", ["gov"], None, "Theater State"),
("Theravada Buddhism", "Buddhism focused on meditation found in Southeast Asia", ["rel"], "ssasia", "Theravada Buddhism"),
("Tibetan Buddhism", "form of Buddhism in Tibet centered around chanting", ["rel"], "eastasia", "Tibetan Buddhism"),
("Trans-Saharan Trade Routes", "networks of exchange that transformed West Africa by connecting it to the larger parts of the world", ["econ"], "africa", "Trans-Saharan Trade Routes"),
("Universalizing Religion", "a religion seeking to convert others. Islam was a universalizing religion", ["rel"], None, "Universalizing Religion"),
("Urdu", "a new language with elements of Hindi, Arabic, and Farsi that developed among the Muslims of South Asia", ["soc"], "ssasia", "Urdu"),
("Varnas", "warriors within the Indian caste system", ["soc"], "ssasia", "Varna"),
("Vedas", "the oldest collection of scriptures of Hinduism and religious texts in an ancient Sanskrit language", ["rel"], "ssasia", "Vedas"),
("Vijayanagara Empire", "an empire in southern India between 1336 and 1646; founded by the brothers Harihara and Bukka Raya in 1336 to protect the people in the southern region from the Muslim states, or sultanates, in the north", ["states"], "ssasia", "Vijayanagara Empire"),
("Vishnu", "Hindu god considered the preserver of the world", ["rel"], "ssasia", "Vishnu"),
("Woodblock Printing", "a technique for printing text, images or patterns used widely throughout East Asia that originated in China", ["econ"], "eastasia", "Woodblock printing"),
("Xiongnu", "the Chinese name for the confederacy of Turkish-speaking peoples who were nomadic herders in Central Asia", ["soc","states"], "eastasia", "Xiongnu"),
]

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode("ascii")
    s = s.lower().replace("&","and")
    s = re.sub(r"[^a-z0-9]+","-", s).strip("-")
    return s

terms = []
rename_map = []
slugs = set()
for term, definition, concepts, region, audiofile in R:
    slug = slugify(audiofile)
    assert slug not in slugs, "duplicate slug: " + slug
    slugs.add(slug)
    for c in concepts:
        assert c in CONCEPTS, "bad concept " + c
    assert region is None or region in REGIONS, "bad region " + str(region)
    terms.append({
        "term": term,
        "definition": definition,
        "concepts": concepts,
        "region": region,
        "audio": slug + ".mp3",
        "sentence": None,
    })
    rename_map.append({"from": audiofile + ".mp3", "to": slug + ".mp3"})

assert len(terms) == 100, "expected 100 terms, got %d" % len(terms)

unit = {
    "id": "unit1",
    "title": "Unit 1: The Global Tapestry",
    "subtitle": "1200\u20131450",
    "concepts": CONCEPTS,
    "regions": REGIONS,
    "terms": terms,
}

os.makedirs("/home/claude/site/data", exist_ok=True)
with open("/home/claude/site/data/unit1.json","w",encoding="utf-8") as f:
    json.dump(unit, f, ensure_ascii=False, indent=2)
with open("/home/claude/site/data/unit1.js","w",encoding="utf-8") as f:
    f.write("window.APWH = window.APWH || {};\n")
    f.write("window.APWH.unit1 = ")
    json.dump(unit, f, ensure_ascii=False, indent=2)
    f.write(";\n")

with open("/home/claude/site_build/audio_rename_map.json","w",encoding="utf-8") as f:
    json.dump(rename_map, f, ensure_ascii=False, indent=2)

placed = sum(1 for t in terms if t["region"])
print("terms:", len(terms))
print("unique audio slugs:", len(slugs))
print("region-placed:", placed, "| region-less:", len(terms)-placed)
from collections import Counter
print("by region:", dict(Counter(t["region"] for t in terms if t["region"])))
