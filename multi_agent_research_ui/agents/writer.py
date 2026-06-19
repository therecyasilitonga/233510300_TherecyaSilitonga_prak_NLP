"""
agents/writer.py
----------------
Writer bertugas mengubah analisis menjadi laporan final
yang terstruktur, profesional, dan enak dibaca.
Ini adalah output akhir yang akan diterima pengguna.
"""

import os
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.6,  # Sedikit lebih kreatif untuk tulisan yang lebih natural
)


def writer_agent(state: dict) -> dict:
    """
    Langkah writer:
    1. Ambil analisis dari state
    2. Tulis laporan final yang terstruktur
    3. Simpan laporan ke state
    """

    log = "[Writer] Mulai menyusun laporan final..."
    print(log)

    topic = state["topic"]
    analysis = state.get("analysis", "")
    tanggal = datetime.now().strftime("%d %B %Y")

    if not analysis:
        return {
            "final_report": "Gagal membuat laporan: tidak ada analisis tersedia.",
            "messages": [log, "[Writer] Tidak ada analisis dari analyst."]
        }

    prompt = f"""Kamu adalah penulis laporan akademis senior dan peneliti profesional.

Berdasarkan analisis komprehensif berikut tentang "{topic}", susunlah sebuah laporan riset yang sangat rinci, mendalam, terstruktur rapi, dan menggunakan gaya bahasa formal ilmiah (seperti skripsi/thesis akademis) dalam Bahasa Indonesia.

ANALISIS YANG TERSEDIA:
{analysis}

Laporan wajib disusun dengan struktur Bab dan Sub-bab akademis berikut secara detail:

════════════════════════════════════════════════════════════════
                     LAPORAN PENELITIAN ILMIAH
Topik Riset : {topic}
Tanggal     : {tanggal}
Sistem      : Multi-Agent Research Assistant (LangGraph + Ollama)
════════════════════════════════════════════════════════════════

BAB I: PENDAHULUAN
1.1 Latar Belakang Masalah
(Jelaskan secara mendalam latar belakang topik riset ini, sejarah singkat, relevansi konteks global/nasional saat ini, dan mengapa masalah/topik ini sangat penting untuk dibahas secara teoretis maupun praktis. Tulis minimal 2-3 paragraf komprehensif)

1.2 Rumusan Masalah
(Identifikasi dan uraikan minimal 3 poin permasalahan utama atau pertanyaan penelitian krusial terkait topik ini)

1.3 Tujuan Penelitian
(Jelaskan tujuan teoretis dan aplikatif dari riset ini secara runut untuk menjawab rumusan masalah)

BAB II: LANDASAN TEORI DAN TEMUAN DATA
2.1 Landasan Konseptual
(Jelaskan konsep dasar, terminologi utama, serta teori dasar yang melandasi topik riset ini secara akademis)

2.2 Temuan Data dan Fakta Lapangan
(Sajikan secara detail seluruh data riset, temuan penting, dan fakta konkret yang diperoleh dari pencarian data primer/sekunder. Klasifikasikan informasi ke dalam poin-poin analisis yang kuat)

2.3 Tabel Ringkasan Data Riset
(Buatlah **Tabel Markdown** yang sangat rapi untuk merangkum temuan data di atas. Gunakan kolom seperti: [Parameter / Karakteristik], [Deskripsi Temuan / Nilai], [Tingkat Urgensi / Dampak])

BAB III: ANALISIS DAN PEMBAHASAN
3.1 Analisis Tren, Karakteristik, dan Dinamika
(Lakukan pembahasan kritis mengenai tren perkembangan saat ini, pola yang terbentuk dari data, serta dinamika yang terjadi di lapangan terkait topik)

3.2 Visualisasi Tren Riset / Grafik Teks (Opsional)
(Sajikan visualisasi data/tren komparatif sederhana menggunakan karakter ASCII/Unicode seperti blok `████████░░ 80%` untuk menggambarkan skala perbandingan data, tren tahunan, proporsi pasar, atau metrik kuantitatif lainnya secara visual HANYA JIKA terdapat data numerik, statistik, atau dataset kuantitatif yang jelas dari analisis di atas. Jika data kuantitatif tersebut tidak tersedia pada sumber riset, bagian sub-bab grafik ini **tidak perlu dibuat / dilewati saja**).

3.3 Implikasi, Dampak, dan Tantangan Utama
(Analisis secara komprehensif apa implikasi logis dari temuan ini bagi sektor terkait, industri, kebijakan, maupun masyarakat umum. Uraikan pula tantangan struktural atau hambatan yang dihadapi berdasarkan data)

BAB IV: KESIMPULAN DAN REKOMENDASI
4.1 Kesimpulan Penelitian
(Tarik kesimpulan akhir secara akademis, objektif, dan menyeluruh yang merangkum esensi bab-bab sebelumnya secara padat namun kaya informasi)

4.2 Rekomendasi Aplikatif
(Berikan rekomendasi konkret dan taktis yang berorientasi pada aksi bagi para praktisi, akademisi, pengambil keputusan, atau pihak terkait lainnya untuk menindaklanjuti temuan penelitian ini)

BAB V: DAFTAR PUSTAKA
(Tuliskan seluruh rujukan, sitasi, dan sumber pustaka secara formal dan akademis. Cantumkan semua URL sumber / situs web yang valid dari Analisis yang Tersedia untuk memudahkan pelacakan dokumen oleh pembaca)

════════════════════════════════════════════════════════════════
Catatan: Laporan akademis ini dihasilkan secara otomatis oleh sistem kecerdasan buatan (AI) berbasis multi-agent. Disarankan untuk memverifikasi data lapangan dengan literatur dan sumber rujukan resmi.
════════════════════════════════════════════════════════════════

Aturan Penulisan:
- Gunakan Bahasa Indonesia Baku (Ejaan Yang Disempurnakan - EYD).
- Gaya penulisan harus akademis, objektif, formal, dan analitis (hindari kata-kata populer/non-baku).
- Setiap Bab dan Sub-bab harus ditulis secara padat informasi, ekspansif, mendalam (panjang dan detail), tidak sekadar ringkasan pendek.
- Wajib menyertakan Tabel Markdown (Sub-bab 2.3). Grafik Teks (Sub-bab 3.2) bersifat opsional dan hanya dibuat jika terdapat data kuantitatif pendukung pada sumber riset.
- Tulis laporan penelitian ini sekarang secara lengkap, terperinci, dan rapi:"""

    print("[Writer] Menulis laporan dengan Ollama...")
    response = llm.invoke([HumanMessage(content=prompt)])
    report = response.content

    log2 = "[Writer] Laporan final selesai ditulis!"
    print(log2)

    return {
        "final_report": report,
        "messages": [log, log2]
    }
