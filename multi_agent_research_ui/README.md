# Multi-Agent Research AI
### UAS NLP/LLM — LangChain + LangGraph + LangSmith + Ollama

Sistem riset otomatis berbasis multi-agent dengan tampilan web profesional.

---

## Cara Menjalankan

### 1. Install Ollama & pull model
```bash
# Download dari https://ollama.com lalu:
ollama pull llama3.2:3b
ollama serve
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup .env
Edit file `.env` — isi `LANGCHAIN_API_KEY` dari smith.langchain.com (gratis)

### 4. Jalankan web app
```bash
streamlit run app.py
```
Buka browser di `http://localhost:8501`

---

## Fitur Aplikasi
- Input topik bebas atau pilih topik cepat
- Status agen real-time (Supervisor, Researcher, Analyst, Writer)
- Tab hasil: Laporan Final, Analisis, Data Riset
- Download laporan sebagai file .txt
- Log aktivitas terminal
- Pilih model Ollama dari sidebar
- Atur temperature & jumlah hasil pencarian

---

## Library Wajib UAS

| Library | Dipakai di file |
|---|---|
| LangChain | `agents/*.py` — ChatOllama, HumanMessage, prompt |
| LangGraph | `graph.py` — StateGraph, node, conditional edges |
| LangSmith | `.env` — LANGCHAIN_TRACING_V2=true |

---

## Struktur Kode
```
multi_agent_research_ui/
├── app.py             ← UI Streamlit (web app)
├── graph.py           ← Alur LangGraph
├── state.py           ← Shared state antar agen
├── agents/
│   ├── supervisor.py
│   ├── researcher.py
│   ├── analyst.py
│   └── writer.py
├── tools/
│   └── search_tool.py
├── requirements.txt
└── .env
```
