"""
app.py
------
Tampilan web profesional untuk sistem Multi-Agent Riset Otomatis.
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── Konfigurasi Halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Kustom ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Font & warna dasar */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sembunyikan elemen bawaan Streamlit */
#MainMenu, footer, header { visibility: hidden; }

/* Header Utama */
.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.main-header h1 {
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    margin: 0;
}
.badge-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.85);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
}

/* Kartu Agen */
.agent-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}
.agent-card.active {
    border-color: #6366f1;
    background: #f8fafc;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
}
.agent-card.done {
    border-color: #10b981;
    background: #f0fdf4;
}
.agent-card.waiting {
    opacity: 0.65;
    background: #fafafa;
}
.agent-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.4rem;
}
.agent-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.agent-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: #1e293b;
    margin: 0;
}
.agent-desc {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-left: auto;
}
.dot-waiting  { background: #cbd5e1; }
.dot-active   { background: #6366f1; animation: pulse 1.5s infinite; }
.dot-done     { background: #10b981; }

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%       { transform: scale(1.2); opacity: 0.4; }
}

/* Empty State */
.empty-state {
    background: #f8fafc;
    border: 2px dashed #e2e8f0;
    border-radius: 12px;
    padding: 4rem 2rem;
    text-align: center;
    color: #64748b;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.empty-state-title {
    font-weight: 600;
    font-size: 1.1rem;
    color: #1e293b;
    margin: 1.2rem 0 0.35rem 0;
}
.empty-state-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    max-width: 340px;
    margin: 0 auto;
}

/* Metrik */
.metric-row {
    display: flex;
    gap: 12px;
    margin: 1.2rem 0;
    flex-wrap: wrap;
}
.metric-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    flex: 1;
    min-width: 130px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.01);
}
.metric-label {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
}

/* Log Terminal */
.log-box {
    background: #0f172a;
    border-radius: 10px;
    padding: 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    max-height: 220px;
    overflow-y: auto;
    line-height: 1.8;
    border: 1px solid #1e293b;
}
.log-line-supervisor { color: #c084fc; }
.log-line-researcher { color: #60a5fa; }
.log-line-analyst    { color: #34d399; }
.log-line-writer     { color: #fb923c; }
.log-line-system     { color: #f8fafc; }

/* Sidebar */
.sidebar-section {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
}
.sidebar-title {
    font-weight: 600;
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 0.8rem;
}

/* Tombol Utama */
.stButton > button {
    background: #4f46e5 !important;
    color: white !important;
    border: 1px solid #4f46e5 !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}
.stButton > button:hover {
    background: #4338ca !important;
    border-color: #4338ca !important;
}

.stDownloadButton > button {
    background: #0f766e !important;
    color: white !important;
    border: 1px solid #0f766e !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: #0d9488 !important;
    border-color: #0d9488 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Ikon SVG untuk Kartu Agen ────────────────────────────────────────────────
SVG_SUPERVISOR = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 16a4 4 0 100-8 4 4 0 000 8z"/><path d="M12 12h.01"/></svg>"""
SVG_RESEARCHER = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>"""
SVG_ANALYST = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>"""
SVG_WRITER = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>"""


# ─── Helper: Render Kartu Agen ─────────────────────────────────────────────────
def agent_card(name, icon, desc, bg, status="waiting"):
    css_class = f"agent-card {status}"
    dot_class = f"dot-{status}"
    status_label = {"waiting": "Menunggu", "active": "Sedang berjalan...", "done": "Selesai"}[status]
    st.markdown(f"""
    <div class="{css_class}">
      <div class="agent-header">
        <div class="agent-icon" style="background:{bg}">{icon}</div>
        <div>
          <p class="agent-title">{name}</p>
          <p class="agent-desc">{desc}</p>
        </div>
        <div class="status-dot {dot_class}" title="{status_label}"></div>
      </div>
      <div style="font-size:0.75rem;color:{'#6366f1' if status=='active' else '#10b981' if status=='done' else '#94a3b8'};font-weight:500;margin-top:2px">
        {status_label}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>Multi-Agent Research Assistant</h1>
  <p>Sistem riset otomatis berbasis AI — cari, analisis, dan tulis laporan dalam sekali klik</p>
  <div class="badge-row">
    <span class="badge">LangChain</span>
    <span class="badge">LangGraph</span>
    <span class="badge">LangSmith</span>
    <span class="badge">Ollama</span>
    <span class="badge">DuckDuckGo Search</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Inisialisasi Session State Topik ──────────────────────────────────────────
if "topic_input" not in st.session_state:
    st.session_state["topic_input"] = ""


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Konfigurasi Sistem")

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Model Ollama</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Pilih model",
        ["llama3.2:3b", "llama3.2:1b", "llama3.1:8b", "mistral", "custom"],
        index=0,
        label_visibility="collapsed"
    )
    if model_choice == "custom":
        model_choice = st.text_input("Nama model custom", placeholder="contoh: phi3:mini")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Pengaturan</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature (kreativitas)", 0.0, 1.0, 0.3, 0.1,
                            help="Lebih tinggi = lebih kreatif, lebih rendah = lebih fokus")
    max_search = st.slider("Jumlah hasil pencarian", 2, 6, 4,
                           help="Berapa banyak hasil web yang dianalisis")
    show_log   = st.toggle("Tampilkan log aktivitas", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Tentang Sistem</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.8rem;color:#64748b;line-height:1.7">
    Sistem ini menggunakan 4 agen AI:<br>
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#8b5cf6;margin-right:6px;"></span><b>Supervisor</b> — koordinator alur<br>
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#3b82f6;margin-right:6px;"></span><b>Researcher</b> — cari di internet<br>
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;margin-right:6px;"></span><b>Analyst</b> — analisis mendalam<br>
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#f97316;margin-right:6px;"></span><b>Writer</b> — tulis laporan final
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Layout Utama ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    topic_placeholder = st.empty()

    # Contoh topik cepat
    st.markdown("<p style='font-size:0.8rem;color:#94a3b8;margin-bottom:6px'>Topik cepat:</p>", unsafe_allow_html=True)
    quick_cols = st.columns(2)
    quick_topics = [
        "Big Data Indonesia 2024",
        "Machine Learning tren terbaru",
        "NoSQL vs SQL perbandingan",
        "AI di dunia pendidikan",
    ]
    for i, qt in enumerate(quick_topics):
        with quick_cols[i % 2]:
            if st.button(qt, key=f"qt_{i}", use_container_width=True):
                st.session_state["topic_input"] = qt
                st.rerun()

    with topic_placeholder.container():
        st.markdown("#### Topik Riset")
        topic = st.text_area(
            "Masukkan topik",
            placeholder="Contoh: Perkembangan Big Data di Indonesia tahun 2024",
            height=100,
            label_visibility="collapsed",
            key="topic_input"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Mulai Riset", use_container_width=True)

    # ── Panel Status Agen ──────────────────────────────────────────────────────
    st.markdown("#### Status Agen")
    status_placeholder = st.empty()

    def render_agents(s_sup="waiting", s_res="waiting", s_ana="waiting", s_wri="waiting"):
        with status_placeholder.container():
            agent_card("Supervisor", SVG_SUPERVISOR, "Koordinator alur kerja", "#ede9fe", s_sup)
            agent_card("Researcher", SVG_RESEARCHER, "Pencarian web otomatis",  "#dbeafe", s_res)
            agent_card("Analyst",    SVG_ANALYST, "Analisis data & insight", "#d1fae5", s_ana)
            agent_card("Writer",     SVG_WRITER, "Penulisan laporan final", "#ffedd5", s_wri)

    render_agents()

with col_right:
    st.markdown("#### Hasil Riset")
    output_placeholder  = st.empty()
    metrics_placeholder = st.empty()
    log_placeholder     = st.empty()

    # Tampilan default sebelum riset dijalankan
    with output_placeholder.container():
        st.markdown("""
        <div class="empty-state">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <div class="empty-state-title">Laporan belum tersedia</div>
          <div class="empty-state-subtitle">Masukkan topik riset di panel kiri dan klik Mulai Riset untuk memulai proses analisis otomatis.</div>
        </div>
        """, unsafe_allow_html=True)


# ─── Proses Riset Saat Tombol Diklik ──────────────────────────────────────────
if run_btn:
    if not topic or not topic.strip():
        st.warning("Harap masukkan topik riset terlebih dahulu.")
        st.stop()

    topic = topic.strip()
    logs  = []
    start = time.time()

    # Update .env model secara runtime
    os.environ["OLLAMA_MODEL"] = model_choice

    try:
        from graph import build_graph

        # ── Tahap 1: Build graph ───────────────────────────────────────────────
        render_agents(s_sup="active")
        with output_placeholder.container():
            st.info("Menginisialisasi sistem multi-agent...")

        app = build_graph()
        logs.append(("system", "Sistem multi-agent berhasil diinisialisasi"))

        # ── Tahap 2: Supervisor Awal ───────────────────────────────────────────
        render_agents(s_sup="active")
        logs.append(("supervisor", "Supervisor menganalisis tugas..."))
        if show_log:
            with log_placeholder.container():
                st.markdown('<div class="log-box">' +
                    "".join(f'<div class="log-line-{t}">{m}</div>' for t, m in logs) +
                    '</div>', unsafe_allow_html=True)

        # ── Tahap 3: Researcher ────────────────────────────────────────────────
        render_agents(s_sup="done", s_res="active")
        with output_placeholder.container():
            st.markdown(f"""
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:1.5rem">
              <p style="font-weight:600;color:#1d4ed8;margin:0 0 0.5rem">
                Researcher sedang melakukan pencarian...
              </p>
              <p style="color:#3b82f6;font-size:0.9rem;margin:0">Topik: <b>{topic}</b></p>
            </div>
            """, unsafe_allow_html=True)
        logs.append(("researcher", f"Mencari informasi: '{topic}'"))

        # ── Tahap 4: Analyst ──────────────────────────────────────────────────
        with output_placeholder.container():
            st.markdown("""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:1.5rem">
              <p style="font-weight:600;color:#15803d;margin:0 0 0.5rem">
                Analyst sedang menganalisis data...
              </p>
              <p style="color:#16a34a;font-size:0.9rem;margin:0">Memproses hasil pencarian...</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Jalankan Graph ─────────────────────────────────────────────────────
        initial_state = {
            "topic": topic,
            "search_results": [],
            "analysis": "",
            "final_report": "",
            "next_agent": "",
            "messages": []
        }

        render_agents(s_sup="done", s_res="active")
        final_state = app.invoke(initial_state)

        elapsed = round(time.time() - start, 1)

        # Update log dari state
        for msg in final_state.get("messages", []):
            if "[Supervisor]"  in msg: logs.append(("supervisor", msg))
            elif "[Researcher]" in msg: logs.append(("researcher", msg))
            elif "[Analyst]"    in msg: logs.append(("analyst",    msg))
            elif "[Writer]"     in msg: logs.append(("writer",     msg))
            else:                       logs.append(("system",     msg))

        # ── Tampilkan Hasil ────────────────────────────────────────────────────
        render_agents(s_sup="done", s_res="done", s_ana="done", s_wri="done")

        report = final_state.get("final_report", "")
        analysis = final_state.get("analysis", "")
        sources  = final_state.get("search_results", [])

        # Metrik
        with metrics_placeholder.container():
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-box">
                <div class="metric-label">Waktu proses</div>
                <div class="metric-value" style="color:#4f46e5">{elapsed}s</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">Sumber data</div>
                <div class="metric-value" style="color:#10b981">{len(sources)}</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">Model</div>
                <div class="metric-value" style="color:#f59e0b;font-size:0.9rem">{model_choice}</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">Status</div>
                <div class="metric-value" style="color:#10b981;font-size:0.9rem">Selesai</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Output laporan
        with output_placeholder.container():
            tab1, tab2, tab3 = st.tabs(["Laporan Final", "Analisis", "Data Riset"])

            with tab1:
                if report:
                    st.markdown(report)
                    st.download_button(
                        "Download Laporan (.txt)",
                        data=report,
                        file_name=f"laporan_{topic[:30].replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.warning("Laporan tidak berhasil dibuat.")

            with tab2:
                if analysis:
                    st.markdown(analysis)
                else:
                    st.info("Analisis tidak tersedia.")

            with tab3:
                if sources:
                    for i, src in enumerate(sources, 1):
                        with st.expander(f"Sumber {i}"):
                            st.write(src)
                else:
                    st.info("Data sumber tidak tersedia.")

        # Log terminal
        if show_log:
            logs.append(("system", f"Proses selesai dalam {elapsed} detik"))
            with log_placeholder.container():
                st.markdown("**Log Aktivitas Agen**")
                st.markdown('<div class="log-box">' +
                    "".join(f'<div class="log-line-{t}">{m}</div>' for t, m in logs) +
                    '</div>', unsafe_allow_html=True)

        st.success(f"Riset selesai dalam {elapsed} detik.")

    except Exception as e:
        render_agents()
        with output_placeholder.container():
            st.error(f"Terjadi kesalahan: {str(e)}")
            st.markdown("""
            **Kemungkinan penyebab:**
            - Aplikasi Ollama belum aktif (jalankan `ollama serve` di terminal)
            - Model yang dipilih belum diunduh (jalankan `ollama pull [nama_model]` di terminal)
            - Koneksi internet tidak stabil (untuk pencarian web)
            """)
        st.exception(e)
