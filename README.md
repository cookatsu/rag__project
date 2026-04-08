# Praxisprojekt: Retrieval-Augmented Generation (RAG) System

In diesem Projekt haben wir ein einfaches System gebaut, das Fragen auf Basis von lokalen Daten beantwortet.  
Es kombiniert eine Suche in Texten mit einem Sprachmodell (LLM), um passende Antworten zu geben.  

## Systemarchitektur

Das System besteht aus folgenden Komponenten:
- **Datenaufbereitung:** Cleaning und Chunking der Quelldaten.
- **Embeddings & Vektordatenbank:** Erzeugung von Vektoren mit `sentence-transformers` und Speicherung in einem `FAISS`-Index.
- **Retrieval:** Suche nach den Top-k relevantesten Kontextabschnitten.
- **LLM-Integration:** Generierung der Antwort mit `Ollama` (Modell: `llama3`).
- **Benutzeroberfläche:** Interaktive Web-App mit `Streamlit`.

## Voraussetzungen

- Python 3.8+
- [Ollama](https://ollama.com/) installiert und im Hintergrund laufend.
___

## Starten

1. Notwendige Bibliotheken installieren:
 ```bash
pip install streamlit sentence-transformers faiss-cpu requests numpy
```
2. Das benötigte LLM-Modell in Ollama laden:
```bash
ollama pull llama3
```
3. Die Benutzeroberfläche (UI) starten:
```bash
python -m streamlit run app.py
```
## Projektstruktur

 app.py → Hauptanwendung und UI.

 embedding_faiss.py → erstellt den Index.  

 faiss_index.index → gespeicherte Daten.
 
 quellen.json → Textdaten.


## Nutzung
Nach dem Start öffnet sich die App im Browser.  
Einfach eine Frage eingeben, und das System gibt eine Antwort mit passenden Quellen zurück.  
