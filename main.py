from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routes import resource, transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inisialisasi tabel database saat server menyala
    await init_db()
    yield

app = FastAPI(
    title="API Toko Buku - UTS Komputasi Paralel",
    description="Implementasi REST API Asinkron dengan FastAPI, aiosqlite, BackgroundTasks, dan asyncio.Lock",
    lifespan=lifespan
)

app.include_router(resource.router)
app.include_router(transaction.router)