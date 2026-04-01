from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
import requests

modell = SentenceTransformer('all-MiniLM-L6-v2')

with open("quellen.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

texte = [eintrag["inhalt"] for eintrag in daten]

index = faiss.read_index("faiss_index.index")

frage = input("Frage eingeben: ")

frage_embedding = modell.encode([frage])
frage_embedding = np.array(frage_embedding).astype('float32')

k = 3
distanzen, indizes = index.search(frage_embedding, k)

kontext = ""
quellen = []

for i in indizes[0]:
    eintrag = daten[i]
    kontext += eintrag["inhalt"] + "\n"
    quellen.append(eintrag["quelle"])

prompt = f"""
Beantworte die Frage basierend nur auf dem Kontext.

Kontext:
{kontext}

Frage:
{frage}

Antwort:
"""

antwort = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
)

print("\nAntwort:\n")
print(antwort.json()["response"])

print("\nQuellen:")
for q in set(quellen):
    print("-", q)