"""
agents/analyst.py
-----------------
Analyst bertugas membaca hasil riset dari Researcher
dan mengubahnya menjadi analisis yang lebih mendalam:
- Apa tren yang terlihat?
- Apa implikasi dari data ini?
- Apa yang perlu diperhatikan?
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.4,
)


def analyst_agent(state: dict) -> dict:
    """
    Langkah analyst:
    1. Baca search_results dari state (hasil kerja researcher)
    2. Lakukan analisis mendalam
    3. Simpan analisis ke state
    """

    log = "[Analyst] Memulai analisis data riset..."
    print(log)

    # Ambil semua hasil riset
    search_results = state.get("search_results", [])
    topic = state["topic"]

    if not search_results:
        return {
            "analysis": "Tidak ada data yang bisa dianalisis.",
            "messages": [log, "[Analyst] Tidak ada data dari researcher."]
        }

    # Gabungkan semua hasil riset
    all_research = "\n\n".join(search_results)

    prompt = f"""Kamu adalah analis senior dan peneliti akademik yang ahli dalam menyusun analisis riset teoritis dan empiris.

Topik riset: "{topic}"

Data hasil riset:
{all_research}

Tugas kamu adalah menyusun analisis komprehensif, terperinci, dan mendalam dalam Bahasa Indonesia formal untuk bahan penulisan skripsi/karya ilmiah. Analisis wajib memuat elemen-elemen berikut:

1. **RINGKASAN EKSEKUTIF MENDALAM** (Analisis komprehensif 1-2 paragraf mengenai urgensi topik dan esensi temuan).
2. **TEMUAN DATA UTAMA & TABEL** (Sajikan perbandingan data atau ringkasan temuan dalam bentuk **Tabel Markdown** yang rapi dengan kolom yang jelas seperti Parameter, Deskripsi/Nilai, dan Dampak).
3. **VISUALISASI TREN / GRAFIK TEKS (OPSIONAL)** (Sajikan visualisasi data/tren komparatif sederhana menggunakan karakter ASCII/Unicode seperti blok `████░░` **HANYA JIKA** terdapat data numerik, statistik, atau dataset kuantitatif yang jelas dari sumber riset di atas. Jika data kuantitatif tersebut tidak tersedia dari sumber, bagian grafik ini **tidak perlu dibuat / dilewati saja**).
4. **TREN, KARAKTERISTIK, DAN POLA** (Analisis mendalam mengenai tren yang terlihat, evolusi pola data, dan faktor-faktor pendorong utama).
5. **IMPLIKASI SEKTORAL DAN STRATEGIS** (Penjelasan rinci mengenai konsekuensi logis dari temuan ini terhadap industri, regulasi/kebijakan pemerintah, maupun bidang akademis terkait).
6. **TANTANGAN DAN CATATAN KRITIS** (Aspek tantangan, limitasi data, hambatan implementasi di lapangan, serta poin penting yang perlu diwaspadai).
7. **DAFTAR PUSTAKA / REFERENSI** (Buatlah daftar rujukan ilmiah formal yang mencakup seluruh URL sumber/situs web yang terdapat di dalam Data hasil riset di atas).

Tulis analisis kamu secara akademis, formal, objektif, terperinci, panjang lebar, dan sertakan tabel serta grafik opsional tersebut secara rapi:"""

    print("[Analyst] Menganalisis dengan Ollama...")
    response = llm.invoke([HumanMessage(content=prompt)])
    analysis = response.content

    log2 = "[Analyst] Analisis selesai."
    print(log2)

    return {
        "analysis": analysis,
        "messages": [log, log2]
    }
