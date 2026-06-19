# Multi-Agent Research AI

Sistem riset otomatis berbasis multi-agent yang mampu mencari, menganalisis, dan menyusun laporan riset hanya dari satu topik yang dimasukkan pengguna. Dibangun menggunakan empat agen AI yang bekerja secara berurutan — **Supervisor**, **Researcher**, **Analyst**, dan **Writer** — dengan model bahasa yang dijalankan secara lokal melalui **Ollama**, tanpa memerlukan API berbayar.

> Proyek ini disusun untuk pemenuhan tugas akhir (UAS) mata kuliah Natural Language Processing / Large Language Model, Program Studi Teknik Informatika, Universitas Islam Riau.

---

## Daftar Isi

- [Tentang Aplikasi](#tentang-aplikasi)
- [Library dan Teknologi yang Digunakan](#library-dan-teknologi-yang-digunakan)
- [Struktur Proyek](#struktur-proyek)
- [Panduan Instalasi Step-by-Step](#panduan-instalasi-step-by-step)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Cara Menggunakan Aplikasi](#cara-menggunakan-aplikasi)
- [Troubleshooting Umum](#troubleshooting-umum)
- [Identitas Pengembang](#identitas-pengembang)

---

## Tentang Aplikasi

**Multi-Agent Research AI** adalah aplikasi web yang mengotomatisasi proses riset menggunakan pendekatan *multi-agent system*. Alih-alih mengandalkan satu prompt besar ke satu model untuk menghasilkan laporan riset, sistem ini membagi pekerjaan ke dalam empat agen yang masing-masing punya tanggung jawab spesifik:

| Agen | Tugas |
|---|---|
| **Supervisor** | Menerima topik dari pengguna dan menyusunnya menjadi rencana riset yang lebih terarah |
| **Researcher** | Mencari informasi dari internet menggunakan tool pencarian, berdasarkan rencana dari Supervisor |
| **Analyst** | Menyaring dan menganalisis data mentah hasil pencarian untuk menemukan insight penting |
| **Writer** | Menyusun seluruh temuan menjadi laporan akhir yang rapi dan mudah dibaca |

Keempat agen ini dijalankan secara **berurutan (sequential)** melalui graf kerja yang didefinisikan menggunakan LangGraph, dan seluruh prosesnya dapat dipantau secara real-time melalui antarmuka web berbasis Streamlit.

---

## Library dan Teknologi yang Digunakan

### 1. LangChain
LangChain adalah framework yang menyediakan komponen-komponen dasar untuk membangun aplikasi berbasis LLM. Dalam proyek ini, LangChain digunakan untuk:
- `ChatOllama` — kelas yang menjadi penghubung antara kode Python dengan model yang berjalan di Ollama.
- `HumanMessage` — struktur standar untuk membungkus pesan/prompt yang dikirim ke model.
- Penyusunan *prompt template* yang membentuk instruksi peran masing-masing agen.

Implementasi: seluruh file di dalam folder `agents/`

### 2. LangGraph
LangGraph dibangun di atas LangChain dan berfungsi sebagai "pengatur lalu lintas" antar-agen. Komponen utama yang dipakai:
- `StateGraph` — struktur graf yang mendefinisikan node (agen) dan urutan eksekusinya.
- *Edge* — penghubung antar-node yang menentukan agen mana yang dijalankan setelah agen sebelumnya selesai.

Implementasi: `graph.py`

### 3. LangSmith
LangSmith adalah platform observabilitas khusus aplikasi LLM. Dengan mengaktifkannya, setiap pemanggilan model oleh keempat agen akan tercatat secara otomatis — termasuk input, output, dan waktu eksekusi — sehingga memudahkan proses debugging dan evaluasi.

Implementasi: diaktifkan lewat variabel `LANGCHAIN_TRACING_V2=true` di file `.env`

### 4. Ollama
Ollama adalah *runtime* yang memungkinkan model bahasa open-source dijalankan secara lokal di komputer, tanpa biaya API. Proyek ini menggunakan model **Llama 3.2 (3B parameter)** sebagai model utama yang menjalankan seluruh proses inferensi teks.

Implementasi: backend inferensi seluruh agen, dipanggil melalui `ChatOllama`

### 5. Streamlit
Streamlit adalah framework Python untuk membangun antarmuka web interaktif tanpa perlu menulis HTML/CSS/JS secara manual. Seluruh tampilan aplikasi — input topik, status agen real-time, hingga tab hasil riset — dibangun menggunakan Streamlit.

Implementasi: `app.py`

### 6. DuckDuckGo Search
Tool pencarian yang digunakan oleh Researcher Agent untuk mengambil data dari internet secara real-time, tanpa memerlukan API key berbayar seperti Google Search API.

Implementasi: `tools/search_tool.py`

---

## Struktur Proyek

```
multi_agent_research_ui/
├── app.py                  ← Antarmuka web (Streamlit) — entry point utama
├── graph.py                ← Definisi alur kerja LangGraph
├── state.py                ← Struktur state yang dibagikan antar-agen
├── main.py                 ← Entry point alternatif (CLI/testing)
├── agents/
│   ├── supervisor.py        ← Logika Supervisor Agent
│   ├── researcher.py        ← Logika Researcher Agent
│   ├── analyst.py            ← Logika Analyst Agent
│   └── writer.py              ← Logika Writer Agent
├── tools/
│   └── search_tool.py        ← Tool pencarian (DuckDuckGo)
├── requirements.txt           ← Daftar dependensi Python
└── .env                        ← Konfigurasi environment variable
```

---

## Panduan Instalasi Step-by-Step

### Langkah 1 — Pastikan Prasyarat Sudah Terpasang

Sebelum mulai, pastikan komputer Anda sudah memiliki:
- **Python 3.10+** — cek dengan `python --version`
- **Git** — cek dengan `git --version`
- Koneksi internet (untuk mengunduh model dan dependensi)

### Langkah 2 — Clone Repository

```bash
git clone https://github.com/therecyasilitonga/233510300_TherecyaSilitonga_prak_NLP.git
cd 233510300_TherecyaSilitonga_prak_NLP
```

### Langkah 3 — Install Ollama

Unduh dan instal Ollama dari situs resmi: **https://ollama.com**

Setelah terinstal, verifikasi dengan:
```bash
ollama --version
```

### Langkah 4 — Unduh Model Llama 3.2 (3B)

```bash
ollama pull llama3.2:3b
```

Tunggu proses unduhan selesai (ukuran model sekitar 2 GB, tergantung koneksi internet).

### Langkah 5 — Jalankan Ollama Server

```bash
ollama serve
```

> **Penting:** Biarkan terminal ini tetap terbuka dan berjalan di latar belakang selama aplikasi digunakan. Jika ditutup, aplikasi tidak akan bisa terhubung ke model.

### Langkah 6 — Buat Virtual Environment (Opsional, tapi disarankan)

Buka terminal baru (terminal yang lain, karena terminal sebelumnya sedang dipakai `ollama serve`), lalu:

```bash
python -m venv venv
```

Aktifkan virtual environment:
```bash
# Windows (PowerShell)
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Langkah 7 — Install Seluruh Dependensi Python

```bash
pip install -r requirements.txt
```

Perintah ini akan menginstal LangChain, LangGraph, LangSmith client, Streamlit, dan seluruh library lain yang tercantum di `requirements.txt` secara otomatis.

### Langkah 8 — Buat Akun LangSmith dan Ambil API Key

1. Buka **https://smith.langchain.com**, daftar menggunakan email (gratis).
2. Setelah login, masuk ke halaman **Settings** → **API Keys**.
3. Klik **Create API Key**, lalu salin key yang muncul.

### Langkah 9 — Konfigurasi File `.env`

Buka file `.env` pada folder utama proyek, lalu isi seperti berikut:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tempel_api_key_anda_di_sini
LANGCHAIN_PROJECT=multi-agent-research-ui
```

Simpan file tersebut.

---

## Menjalankan Aplikasi

Pastikan **Ollama masih berjalan** (`ollama serve` masih aktif di terminal lain), lalu jalankan:

```bash
streamlit run app.py
```

Setelah perintah dijalankan, Streamlit akan menampilkan output seperti berikut di terminal:

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Browser akan terbuka secara otomatis. Jika tidak, salin alamat `http://localhost:8501` secara manual ke browser Anda.

---

## Cara Menggunakan Aplikasi

1. **Atur konfigurasi** di sidebar kiri — pilih model Ollama, atur *temperature* (disarankan 0.3 untuk hasil yang lebih faktual), dan tentukan jumlah hasil pencarian.
2. **Masukkan topik riset** pada kolom "Topik Riset", atau klik salah satu tombol "Topik cepat" yang sudah disediakan.
3. Klik tombol **"Mulai Riset"**.
4. Amati panel **"Status Agen"** — status setiap agen akan berubah dari "Menunggu" → "Sedang berjalan..." → "Selesai" secara berurutan.
5. Setelah seluruh proses selesai, hasil dapat dilihat melalui tiga tab di panel "Hasil Riset":
   - **Laporan Final** — narasi hasil riset
   - **Analisis** — insight dari Analyst Agent
   - **Data Riset** — data mentah hasil pencarian
6. Klik tombol unduh untuk menyimpan laporan dalam format `.txt`.

---

## Troubleshooting Umum

| Masalah | Kemungkinan Sebab | Solusi |
|---|---|---|
| `ollama` tidak dikenali di terminal | Ollama belum terinstal atau PATH belum terdaftar | Instal ulang dari ollama.com, lalu restart terminal |
| Aplikasi error "connection refused" ke Ollama | `ollama serve` belum dijalankan | Jalankan `ollama serve` di terminal terpisah sebelum `streamlit run app.py` |
| Proses riset sangat lambat | Model berukuran besar untuk spesifikasi komputer yang terbatas | Gunakan model lebih kecil atau kurangi jumlah hasil pencarian |
| Tracing tidak muncul di LangSmith | API key salah atau `LANGCHAIN_TRACING_V2` belum `true` | Periksa kembali isi file `.env` |
| `ModuleNotFoundError` saat `streamlit run app.py` | Dependensi belum terinstal atau virtual environment belum aktif | Jalankan ulang `pip install -r requirements.txt` setelah mengaktifkan venv |

---

## Identitas Pengembang

**Nama:** Therecya Silitonga
**NPM:** 233510300
**Program Studi:** Teknik Informatika
**Universitas:** Universitas Islam Riau
**Mata Kuliah:** Natural Language Processing / Large Language Model (UAS)

---

> Dikembangkan sebagai bagian dari tugas akhir mata kuliah NLP/LLM, menerapkan konsep agentic AI workflow menggunakan LangGraph dengan model LLM lokal melalui Ollama.
