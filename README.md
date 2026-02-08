# bike-sharing

Analisis dataset Bike Sharing menggunakan Python (Pandas, Plotly) dan visualisasi interaktif dengan Streamlit

- Akses melalui: [Bike Sharing Analytics](https://bikeshareanalysis.streamlit.app/)

## Setup Environment - Anaconda

```text
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Fitur Utama

- **KPI Metrics:** Ringkasan total peminjaman, rata-rata harian, dan kondisi cuaca ekstrem.
- **Analisis Cuaca:** Visualisasi korelasi antara suhu, kelembapan, dan kecepatan angin terhadap jumlah peminjam.
- **Analisis Musiman:** Perbandingan perilaku pengguna di berbagai musim.
- **Segmentasi (Clustering):** Pengelompokan kondisi cuaca (Perfect Ride, Comfortable, Challenging) untuk melihat potensi lonjakan pengguna.

## Struktur Folder

```text
.
├── dashboard/
│   ├── dashboard.py       # File utama dashboard Streamlit
│   └── day.csv            # Dataset yang telah dibersihkan
├── data/
│   └── day.csv            # Dataset mentah (opsional)
├── notebook.ipynb         # Proses analisis data (EDA)
├── README.md              # Dokumentasi proyek
└── requirements.txt       # Daftar library yang dibutuhkan
```

## Menjalankan Project

```bash
# Clone repository
git clone https://github.com/t-sofiachairani/bike-sharing.git
cd bike-sharing

# Setup Environment
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

# Run Dashboard
streamlit run dashboard.py
```
