import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
import requests

class RAGSystem:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2', index_path="faiss_index.index", data_path="quellen.json"):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def get_context(self, query, k=5):
        #embediing für die nutzerfrage
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        #ähnl stelle im faiss finden
        distances, indices = self.index.search(query_embedding, k)
        context_parts = []
        sources = []
        for i in indices[0]:
            eintrag = self.data[i]
            context_parts.append(eintrag["inhalt"])
            sources.append({    
                  "quelle": eintrag["quelle"],
                  "titel": eintrag["titel"],
                 "url": eintrag["url"]
        })   
        return context_parts, sources

    def generate_answer(self, query, context_text, ollama_model="llama3"):
        prompt = f"""
        Beantworte die Frage nur anhand des Kontexts.
        Wenn du dir nicht sicher bist oder es nicht im Kontext steht sag, dass du es nicht weißt.
        Kontext:
        {context_text}
        Frage:
        {query}
        Antwort:
        """
        try:
            #anfrage an ollama schicken
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": ollama_model, "prompt": prompt, "stream": False},
                timeout=60
             )
            return response.json().get("response", "Keine Antwort erhalten.")
        except Exception:
            return "Fehler: Verbindung zu Ollama fehlgeschlagen."

def main():
    st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="💬", layout="centered")
  

    st.title("Nachhaltige Mode – Frageassistent")
    st.caption("Antworten basierend auf ausgewählten Quellen zur Textilindustrie")
    @st.cache_resource
    def init_rag():
        return RAGSystem()

    try:
        rag = init_rag()
    except Exception as e:
        st.error(f"Systemfehler beim Laden der Daten: {e}")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("Verwendete Quellen"):
                    for s in message["sources"]:
                        st.write(f"- {s['titel']} ({s['quelle']})")
                        st.write(s["url"])
#generiert antwort
    if prompt := st.chat_input("Ihre Frage zur nachhaltigen Mode..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Suche relevante Informationen..."):
                context_parts, sources = rag.get_context(prompt)
                answer = rag.generate_answer(prompt, "\n".join(context_parts))
                
                st.markdown(answer)
                
                unique_sources = []
                seen_urls = set()

                for s in sources:
                    if s["url"] not in seen_urls:
                        unique_sources.append(s)
                        seen_urls.add(s["url"])

                
                if unique_sources:
                    with st.expander("Verwendete Quellen"):
                        for s in unique_sources:
                            st.write(f"- {s['titel']} ({s['quelle']})")
                            st.write(s["url"])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": unique_sources
                })

if __name__ == "__main__":
    main()
