# from pycdsl import CDSLCorpus
# from pycdsl import corpus
from pycdsl.corpus import CDSLCorpus


from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from bs4 import BeautifulSoup

vowel_signs = {
    "ा": "ā",  # U+093E
    "ि": "i",  # U+093F
    "ी": "ī",  # U+0940
    "ु": "u",  # U+0941
    "ू": "ū",  # U+0942
    "े": "e",  # U+0947
    "ै": "ai", # U+0948
    "ो": "o",  # U+094B
    "ौ": "au", # U+094C
    "": "a"    # No sign = inherent vowel अ
}

def merge_consonant_vowel(consonant_with_halant, vowel_sign):
    if vowel_sign == "":
        # Remove halant to restore inherent vowel अ
        return consonant_with_halant.replace("्", "")
    else:
        return consonant_with_halant + vowel_sign


def ipa_to_iast(ipa_input):
    # Simple IPA to IAST mapping (expand as needed)
    ipa_map = {
        't̪': 't',  # Dental plosive
        'ʈ': 'ṭ',   # Retroflex plosive
        'd̪': 'd',
        'ɖ': 'ḍ',
        'ṭʰ': 'ṭh',
        'tʰ': 'th',
        'ḍʰ': 'ḍh',
        'dʰ': 'dh',
        'ŋ': 'ṅ',
        'ɲ': 'ñ',
        'ɳ': 'ṇ',
        'ʂ': 'ṣ',
        'ɭ': 'ḷ',
        'ʋ': 'v',
        'j': 'j',
        'y': 'y',
        'a': 'a',
        'ā': 'ā',
        'i': 'i',
        'ī': 'ī',
        'u': 'u',
        'ū': 'ū'
    }
    parts = ipa_input.split(',')
    iast_cluster = ''.join(ipa_map.get(p.strip(), p.strip()) for p in parts)
    return iast_cluster

def search_sanskrit(cluster):
    cdsl = CDSLCorpus()
    cdsl.setup(["MW"])  # Monier-Williams dictionary
    # print(corpus.available())  # Lists all registered corpora
    # print(cdsl.get_available_dicts())  # ✅ Lists all corpora you can load
    # print(cdsl.dicts)                  # ✅ Shows currently loaded ones
    # print(dir(cdsl))

    


    # mw = corpus("mw")  # or Corpus.load("mw") depending on version
    results = cdsl.search(cluster)
    print("RAW RESULTS:", results)
    print("TYPE:", type(results))

    # results = mw.search(cluster)

    # results = cdsl.MW.search(cluster)

    print(f"Found {len(results)} entries")
    print(f"Your results for {cluster}:")
    # for entry in results[:10]:  # Show top 10 for brevity
    entries = results.get("MW", [])
    for i, entry in enumerate(entries):
        if i >= 10:
            break
        # process entry here

        # word = entry.get("key", "")
        # print(dir(entry))
        print("TYPE:", type(entry))
        print("VALUE:", entry)


        # word = entry.key  # or entry.headword, depending on the library

        # meaning = entry.get("data", {}).get("definition", "")
        # meaning = entry.data.get("definition", "")
        # print("DATA TYPE:", type(entry.data))
        # print("DATA VALUE:", entry.data)


        html = entry.data  # this is your HTML string
        soup = BeautifulSoup(html, "html.parser")

        # Extract the headword
        key1 = soup.find("key1").text if soup.find("key1") else ""
        key2 = soup.find("key2").text if soup.find("key2") else ""

        # Extract the body content
        body = soup.find("body")
        sanskrit_word = body.find("s").text if body and body.find("s") else ""
        reference = body.text.strip() if body else ""

        print("Headword:", key1)
        print("Alternate:", key2)
        print("Sanskrit:", sanskrit_word)
        print("Reference:", reference)
        # meaning = getattr(entry, "data", {}).get("definition", "")
        # print("Word:", entry.key)
        # print("Meaning:", entry.data.get("definition", ""))
        # print(f"{word}\t{meaning}")

# Example usage
# ipa_input = "t̪,ya"
# iast_cluster = ipa_to_iast(ipa_input)
# search_sanskrit(iast_cluster)
devanagari_consonant = "त्"  # Pure consonant 't̪' in Devanagari
base_consonant = "त्"
for sign, label in vowel_signs.items():
    cluster = merge_consonant_vowel(base_consonant, sign)
    print(f"{cluster} → {label}")
    # Search all Sanskrit words starting with this consonant
    search_sanskrit(cluster)



