from fastapi import APIRouter, BackgroundTasks, HTTPException, status
import asyncio
import aiosqlite
from database import DB_NAME
from models import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Inisialisasi asyncio.Lock untuk mencegah race condition saat pemotongan stok
stok_lock = asyncio.Lock()

# Fungsi pemotongan stok AMAN menggunakan asyncio.Lock
async def potong_stok_dengan_lock(book_id: int, qty: int) -> bool:
    # Critical section dikunci agar hanya 1 coroutine yang memeriksa & memotong stok pada satu waktu
    async with stok_lock:
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("SELECT stok FROM books WHERE id = ?", (book_id,)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return False
                stok_terkini = row[0]

            # Simulasi jeda I/O untuk menguji keamanan lock
            await asyncio.sleep(0.01)

            if stok_terkini < qty:
                return False

            await db.execute("UPDATE books SET stok = stok - ? WHERE id = ?", (qty, book_id))
            await db.commit()
            return True

# Fungsi pekerja latar belakang (asinkron)
async def proses_transaksi_background(trx_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        # 1. Ubah status menjadi processing
        await db.execute("UPDATE transactions SET status = 'processing' WHERE id = ?", (trx_id,))
        await db.commit()

    # 2. Simulasi pemrosesan I/O intensif selama 3 detik
    await asyncio.sleep(3)

    # 3. Finalisasi status menjadi completed
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE transactions SET status = 'completed' WHERE id = ?", (trx_id,))
        await db.commit()

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_transaction(data: TransactionCreate, bg: BackgroundTasks):
    # Cek apakah buku ada di database
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id FROM books WHERE id = ?", (data.book_id,)) as cursor:
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Buku tidak ditemukan")

    # Potong stok dengan pengaman lock
    berhasil = await potong_stok_dengan_lock(data.book_id, data.qty)
    if not berhasil:
        raise HTTPException(status_code=409, detail="Stok buku habis atau tidak mencukupi")

    # Simpan transaksi dengan status awal 'pending'
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO transactions (book_id, qty, status) VALUES (?, ?, 'pending')",
            (data.book_id, data.qty)
        )
        await db.commit()
        trx_id = cursor.lastrowid

    # Jalankan pemrosesan status di latar belakang tanpa memblokir respon HTTP
    bg.add_task(proses_transaksi_background, trx_id)

    return {"id": trx_id, "status": "pending", "message": "Transaksi diterima dan sedang diproses"}

@router.get("", response_model=list[TransactionResponse])
async def get_all_transactions(status: str | None = None):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        if status:
            query = "SELECT * FROM transactions WHERE status = ?"
            params = (status,)
        else:
            query = "SELECT * FROM transactions"
            params = ()
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM transactions WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
            return dict(row)