import asyncio
import aiosqlite
from database import DB_NAME, init_db

DATA_AWAL = [
    ("Algoritma & Pemrograman", "Rinaldi Munir", "Komputer", 95000, 10),
    ("Sistem Terdistribusi", "Andrew Tanenbaum", "Komputer", 150000, 5),
    ("Clean Code", "Robert C. Martin", "Pemrograman", 180000, 8),
    ("Laskar Pelangi", "Andrea Hirata", "Novel", 85000, 15),
    ("Bumi Manusia", "Pramoedya Ananta Toer", "Sastra", 110000, 12),
    ("Filosofi Teras", "Henry Manampiring", "Pengembangan Diri", 90000, 20),
    ("Atomic Habits", "James Clear", "Pengembangan Diri", 105000, 14),
    ("Jaringan Komputer", "Behrouz Forouzan", "Komputer", 130000, 7),
    ("Basis Data", "Fathansyah", "Komputer", 88000, 9),
    ("Laut Bercerita", "Leila S. Chudori", "Novel", 98000, 11),
]

async def seed():
    await init_db()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executemany(
            "INSERT INTO books (judul, penulis, kategori, harga, stok) VALUES (?, ?, ?, ?, ?)",
            DATA_AWAL
        )
        await db.commit()
    print("Berhasil memasukkan 10 data buku awal!")

if __name__ == "__main__":
    asyncio.run(seed())