"""
state.py
--------
Ini adalah 'papan tulis bersama' yang dibaca dan ditulis oleh semua agen.
Bayangkan ini seperti dokumen Google Docs yang bisa diakses semua anggota tim.
"""

from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    # Topik riset yang diminta pengguna
    topic: str

    # Hasil pencarian dari Researcher agent (list of strings)
    search_results: Annotated[List[str], operator.add]

    # Hasil analisis dari Analyst agent
    analysis: str

    # Laporan final dari Writer agent
    final_report: str

    # Keputusan supervisor: siapa yang harus jalan berikutnya
    next_agent: str

    # Log aktivitas setiap agen (untuk debug dan LangSmith)
    messages: Annotated[List[str], operator.add]
