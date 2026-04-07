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
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
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
        Beantworte die Frage basierend nur auf dem bereitgestellten Kontext.
        Falls die Antwort nicht im Kontext steht, sage dass du es nicht weißt.
        Kontext:
        {context_text}
        Frage:
        {query}
        Antwort:
        """
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": ollama_model, "prompt": prompt, "stream": False},
                timeout=60
             )
            return response.json().get("response", "Keine Antwort erhalten.")
        except:
            return "Fehler: Verbindung zu Ollama fehlgeschlagen."

def main():
    st.set_page_config(page_title="RAG Knowledge Assistant", page_icon="💬", layout="centered")
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("💬 RAG Knowledge Assistant")
    st.caption("KI-gestützte Antworten basierend auf Ihrer Wissensdatenbank")

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

    if prompt := st.chat_input("Stellen Sie eine Frage..."):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Suche läuft..."):
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
