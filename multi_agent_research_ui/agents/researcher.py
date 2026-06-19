"""
agents/researcher.py
--------------------
Researcher bertugas mencari informasi di internet tentang topik yang diminta.
Dia pakai web search tool, lalu minta Ollama untuk merangkum hasilnya.
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.search_tool import get_search_tool, run_search

load_dotenv()

# Inisialisasi model Ollama
# Ganti nama model sesuai yang sudah kamu pull (llama3.2, mistral, dll)
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.3,  # Lebih rendah = lebih fokus dan konsisten
)

# Inisialisasi search tool (Tavily atau DuckDuckGo)
search_tool = get_search_tool()


def researcher_agent(state: dict) -> dict:
    """
    Langkah researcher:
    1. Ambil topik dari state
    2. Cari informasi di web
    3. Minta Ollama untuk merangkum hasil pencarian
    4. Simpan rangkuman ke state
    """

    topic = state["topic"]
    log = f"[Researcher] Mencari informasi tentang: '{topic}'"
    print(log)

    # Step 1: Cari di web
    print("[Researcher] Menjalankan web search...")
    raw_results = run_search(search_tool, topic)

    if not raw_results:
        raw_results = [f"Tidak ditemukan hasil pencarian untuk topik: {topic}"]

    # Gabungkan semua hasil pencarian
    combined_results = "\n\n---\n\n".join(raw_results)

    # Step 2: Minta Ollama merangkum hasil pencarian
    print("[Researcher] Merangkum hasil pencarian dengan Ollama...")

    prompt = f"""Kamu adalah peneliti yang handal dan teliti. 
Berikut adalah hasil pencarian web tentang topik "{topic}":

{combined_results}

Tugas kamu:
- Baca semua hasil di atas dengan teliti.
- Identifikasi fakta-fakta penting, angka, data kuantitatif/kualitatif, serta catat URL sumber dari masing-masing informasi tersebut.
- Tulis rangkuman komprehensif dalam Bahasa Indonesia yang menjelaskan hasil pencarian ini secara jelas.
- Di akhir rangkuman, buatlah bagian "DAFTAR SUMBER RUJUKAN" yang mencantumkan seluruh URL sumber unik yang kamu temukan di atas untuk digunakan oleh analis berikutnya.

Tulis hasil riset dan daftar sumber rujukan kamu sekarang:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    summary = response.content

    log2 = f"[Researcher] Selesai. Berhasil merangkum {len(raw_results)} sumber."
    print(log2)

    return {
        "search_results": [summary],
        "messages": [log, log2]
    }
