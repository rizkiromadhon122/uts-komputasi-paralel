from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    judul: str = Field(..., min_length=1)
    penulis: str = Field(..., min_length=1)
    kategori: str = Field(..., min_length=1)
    harga: float = Field(..., gt=0)
    stok: int = Field(..., ge=0)

class BookResponse(BookCreate):
    id: int

class TransactionCreate(BaseModel):
    book_id: int
    qty: int = Field(..., gt=0)

class TransactionResponse(BaseModel):
    id: int
    book_id: int
    qty: int
    status: str