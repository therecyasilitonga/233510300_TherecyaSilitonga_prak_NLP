"""
main.py
-------
File utama untuk menjalankan sistem Multi-Agent Riset Otomatis.

Cara menjalankan:
    python main.py

Atau dengan topik custom dari command line:
    python main.py "Perkembangan AI di Indonesia 2024"
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables dari .env
load_dotenv()

# Setup LangSmith tracing (otomatis aktif jika env var tersedia)
if os.getenv("LANGCHAIN_API_KEY") and not os.getenv("LANGCHAIN_API_KEY").startswith("ls__isi"):
    print("[LangSmith] Tracing aktif — buka smith.langchain.com untuk melihat log")
else:
    print("[LangSmith] API key belum diset — tracing dinonaktifkan")
    os.environ["LANGCHAIN_TRACING_V2"] = "false"

from graph import build_graph


def print_separator(char="═", width=60):
    print(char * width)


def run_research(topic: str):
    """Jalankan sistem multi-agent untuk topik yang diberikan."""

    print_separator()
    print("  SISTEM MULTI-AGENT RISET OTOMATIS")
    print("  LangChain + LangGraph + LangSmith + Ollama")
    print_separator()
    print(f"\nTopik riset: {topic}\n")
    print_separator("─")
    print()

    # Build graph
    app = build_graph()
    print()

    # State awal — hanya topik yang diisi, sisanya kosong
    initial_state = {
        "topic": topic,
        "search_results": [],
        "analysis": "",
        "final_report": "",
        "next_agent": "",
        "messages": []
    }

    print("[Main] Memulai proses riset...\n")
    print_separator("─")
    print()

    # Jalankan graph — ini yang mengaktifkan semua agen secara berurutan
    final_state = app.invoke(initial_state)

    # Tampilkan hasil akhir
    print()
    print_separator()
    print("  HASIL RISET SELESAI")
    print_separator()
    print()
    print(final_state.get("final_report", "Tidak ada laporan yang dihasilkan."))
    print()
    print_separator()

    # Tampilkan log aktivitas semua agen
    print("\nLog aktivitas agen:")
    for msg in final_state.get("messages", []):
        print(f"  {msg}")

    print()
    print("[Selesai] Cek LangSmith untuk melihat trace lengkap setiap agen!")

    return final_state


if __name__ == "__main__":
    # Ambil topik dari argumen command line, atau pakai default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        # Topik default — ganti sesuai kebutuhan kamu
        topic = "Perkembangan Big Data dan Machine Learning di Indonesia tahun 2024"

    run_research(topic)
