Link Video Presentasi: [https://youtu.be/fdVzBfBcF1k?si=5-gnz_aMxueCfQN5]

# API Toko Buku - UTS Komputasi Paralel dan Terdistribusi

## Cara Instalasi
1. Buat virtual environment: `python -m venv venv`
2. Aktifkan virtual environment: `venv\Scripts\activate` (Windows) atau `source venv/bin/activate` (Mac/Linux)
3. Instal dependensi: `pip install -r requirements.txt`
4. Isi data awal: `python seed.py`

## Cara Menjalankan Server
- Mode normal / 1 worker: `uvicorn main:app --workers 1 --port 8000`
- Mode 4 worker: `uvicorn main:app --workers 4 --port 8000`
- Buka dokumentasi interaktif (Swagger UI) di browser: `http://127.0.0.1:8000/docs`