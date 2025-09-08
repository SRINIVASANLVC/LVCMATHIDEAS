# from pycdsl import CDSLCorpus
# from pycdsl import corpus
from pycdsl.corpus import CDSLCorpus
import pandas as pd
from bs4 import BeautifulSoup

cdsl = CDSLCorpus()
cdsl.setup(["MW"])  # Monier-Williams dictionary

cdsl.search_mode = "prefix"
all_words = cdsl.search("क्")  # Empty string to get everything
mw_entries = all_words.get("MW", [])
print("Total entries found:", len(mw_entries))
rows = []
for entry in mw_entries:
    soup = BeautifulSoup(entry.data, "html.parser")
    key1 = soup.find("key1").text if soup.find("key1") else ""
    body = soup.find("body")
    definition = body.text.strip() if body else ""
    rows.append({
        "Headword": key1,
        "Sanskrit": entry.key,
        "Definition": definition
    })

df = pd.DataFrame(rows)
df.to_excel("monier_williams_dump.xlsx", index=False)




