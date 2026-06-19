"""
tools/search_tool.py
--------------------
Tool pencarian web. Pakai Tavily kalau ada API key-nya,
kalau tidak ada otomatis pakai DuckDuckGo (gratis, tanpa API key).
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_search_tool():
    """
    Pilih search tool otomatis:
    - Tavily jika TAVILY_API_KEY tersedia
    - DuckDuckGo (ddgs) sebagai fallback gratis
    """
    tavily_key = os.getenv("TAVILY_API_KEY", "")

    if tavily_key and not tavily_key.startswith("tvly_isi"):
        print("[Search] Menggunakan Tavily Search")
        from langchain_community.tools.tavily_search import TavilySearchResults
        return TavilySearchResults(max_results=4)
    else:
        print("[Search] Menggunakan DuckDuckGo (ddgs)")
        return "ddg"


def run_search(tool, query: str) -> list:
    """
    Jalankan pencarian dan kembalikan hasil sebagai list string.
    Menangani perbedaan format output Tavily vs DuckDuckGo dengan menyertakan URL sumber langsung.
    """
    if tool == "ddg":
        from ddgs import DDGS
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=4))
                formatted = []
                for r in results:
                    url = r.get("href", "Pencarian Web")
                    content = r.get("body", "")
                    title = r.get("title", "Artikel")
                    formatted.append(f"Sumber URL: {url}\nJudul: {title}\nKonten: {content}")
                return formatted
        except Exception as e:
            print(f"[Search] Error DuckDuckGo: {e}")
            return [f"Sumber URL: Pencarian Web\nKonten: Gagal mengambil data search."]

    # Tavily
    results = tool.invoke(query)

    # Tavily mengembalikan list of dict
    if isinstance(results, list):
        formatted = []
        for r in results:
            url = r.get("url", "Pencarian Web")
            content = r.get("content", str(r))
            formatted.append(f"Sumber URL: {url}\nKonten: {content}")
        return formatted

    return [f"Sumber URL: Pencarian Web\nKonten: {str(results)}"]
