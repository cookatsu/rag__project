from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

modell = SentenceTransformer('all-MiniLM-L6-v2')

with open("quellen.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

texte = [eintrag["inhalt"] for eintrag in daten]

embeddings = modell.encode(texte)
embeddings = np.array(embeddings).astype('float32')

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "faiss_index.index")