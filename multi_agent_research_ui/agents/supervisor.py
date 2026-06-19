"""
agents/supervisor.py
--------------------
Supervisor adalah otak dari sistem ini.
Dia yang memutuskan agen mana yang harus bekerja berikutnya
berdasarkan kondisi 'papan tulis' (state) saat ini.

Di sini kita TIDAK pakai LLM — logika supervisor cukup pakai
kondisi sederhana supaya lebih cepat dan hemat resource.
"""


def supervisor_agent(state: dict) -> dict:
    """
    Supervisor memutuskan alur kerja berdasarkan isi state:
    1. Belum ada search_results → suruh researcher
    2. Sudah ada search_results tapi belum ada analysis → suruh analyst
    3. Sudah ada analysis tapi belum ada final_report → suruh writer
    4. Semua sudah ada → selesai (END)
    """

    search_done = bool(state.get("search_results"))
    analysis_done = bool(state.get("analysis", "").strip())
    report_done = bool(state.get("final_report", "").strip())

    if not search_done:
        decision = "researcher"
        log = "[Supervisor] Belum ada data riset. Mengirim ke Researcher..."

    elif not analysis_done:
        decision = "analyst"
        log = "[Supervisor] Data riset sudah ada. Mengirim ke Analyst..."

    elif not report_done:
        decision = "writer"
        log = "[Supervisor] Analisis sudah ada. Mengirim ke Writer..."

    else:
        decision = "END"
        log = "[Supervisor] Semua tahap selesai. Laporan siap!"

    print(log)

    return {
        "next_agent": decision,
        "messages": [log]
    }
