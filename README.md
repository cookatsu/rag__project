# Praxisprojekt: Retrieval-Augmented Generation (RAG) System

Dieses Projekt implementiert ein funktionsfähiges RAG-System, das Antworten auf Fragen basierend auf einer lokalen Wissensbasis generiert. Es kombiniert semantische Suche mit einem lokalen Large Language Model (LLM).

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

## Installation & Ausführung

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

 app.py: Hauptanwendung mit der Klasse RAGSystem und der Streamlit-UI.

 faiss_index.index: Die indizierten Vektordaten.

 quellen.json: Die aufbereiteten Textabschnitte und Metadaten.
 
 embedding_faiss.py: Skript zur Erstellung des Index.


## Nutzung
Nach dem Start der UI über den Browser können Fragen im Textfeld eingegeben werden. Das System sucht automatisch nach relevanten Informationen in der Wissensbasis und liefert eine durch das LLM generierte Antwort inklusive der verwendeten Quellenangaben.
