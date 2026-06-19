"""
graph.py
--------
Di sinilah semua agen dirakit menjadi satu sistem yang bekerja bersama.
LangGraph yang mengatur alur, urutan, dan kondisi perpindahan antar agen.

Analoginya: ini adalah "denah kantor" yang menentukan:
- Siapa yang duduk di mana (node)
- Siapa yang lapor ke siapa (edges)
- Kapan pekerjaan dianggap selesai (END)
"""

from langgraph.graph import StateGraph, END
from state import ResearchState
from agents.supervisor import supervisor_agent
from agents.researcher import researcher_agent
from agents.analyst import analyst_agent
from agents.writer import writer_agent


def route_by_supervisor(state: dict) -> str:
    """
    Fungsi ini dibaca LangGraph untuk memutuskan
    ke node mana alur harus pergi berikutnya.
    Nilai kembali harus cocok dengan kunci di conditional_edges.
    """
    return state.get("next_agent", "END")


def build_graph():
    """
    Membangun dan mengkompilasi graph multi-agent.
    Kembalikan app yang siap dijalankan dengan .invoke()
    """

    # 1. Buat graph kosong dengan state yang sudah kita definisikan
    graph = StateGraph(ResearchState)

    # 2. Daftarkan semua node (agen)
    #    Format: graph.add_node("nama_node", fungsi_agen)
    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("writer", writer_agent)

    # 3. Tentukan titik awal graph
    graph.set_entry_point("supervisor")

    # 4. Tambahkan conditional edges dari supervisor
    #    Artinya: setelah supervisor jalan, tanya fungsi route_by_supervisor
    #    untuk tahu harus pergi ke node mana
    graph.add_conditional_edges(
        "supervisor",           # dari node ini
        route_by_supervisor,    # fungsi yang memutuskan kemana
        {                       # peta keputusan → node tujuan
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "END": END
        }
    )

    # 5. Setelah tiap agen selesai, selalu kembali ke supervisor
    #    Supervisor yang akan memutuskan langkah berikutnya
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("analyst", "supervisor")
    graph.add_edge("writer", "supervisor")

    # 6. Compile graph menjadi app yang bisa dijalankan
    app = graph.compile()

    print("[Graph] Graph berhasil dibangun!")
    print("[Graph] Alur: supervisor → researcher → supervisor → analyst → supervisor → writer → END")

    return app
