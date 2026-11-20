import aiosqlite

DB_NAME = "toko_buku.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Tabel resource utama (minimal 4 kolom selain id + 1 kolom kuantitas/stok)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                penulis TEXT NOT NULL,
                kategori TEXT NOT NULL,
                harga REAL NOT NULL,
                stok INTEGER NOT NULL CHECK (stok >= 0)
            )
        """)
        # Tabel transaksi
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        """)
        await db.commit()