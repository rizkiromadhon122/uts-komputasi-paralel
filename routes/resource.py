from fastapi import APIRouter, HTTPException, status
import aiosqlite
from database import DB_NAME
from models import BookCreate, BookResponse

router = APIRouter(prefix="/resource", tags=["Books (Resource Utama)"])

@router.get("", response_model=list[BookResponse])
async def get_all_books(skip: int = 0, limit: int = 10):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@router.get("/{id}", response_model=BookResponse)
async def get_book(id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM books WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
            return dict(row)

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO books (judul, penulis, kategori, harga, stok) VALUES (?, ?, ?, ?, ?)",
            (book.judul, book.penulis, book.kategori, book.harga, book.stok)
        )
        await db.commit()
        return {**book.model_dump(), "id": cursor.lastrowid}

@router.put("/{id}", response_model=BookResponse)
async def update_book(id: int, book: BookCreate):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "UPDATE books SET judul=?, penulis=?, kategori=?, harga=?, stok=? WHERE id=?",
            (book.judul, book.penulis, book.kategori, book.harga, book.stok, id)
        )
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        return {**book.model_dump(), "id": id}

@router.delete("/{id}")
async def delete_book(id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("DELETE FROM books WHERE id = ?", (id,))
        await db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        return {"message": f"Buku dengan ID {id} berhasil dihapus permanen"}