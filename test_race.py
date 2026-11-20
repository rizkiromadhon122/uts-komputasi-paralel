import asyncio
import httpx

async def main():
    url = "http://127.0.0.1:8000/transactions"
    payload = {"book_id": 1, "qty": 1}

    async with httpx.AsyncClient() as client:
        # Kirim 2 request bersamaan dalam milidetik yang sama
        req1 = client.post(url, json=payload)
        req2 = client.post(url, json=payload)
        res1, res2 = await asyncio.gather(req1, req2)

        print("Respon Request 1:", res1.status_code, res1.json())
        print("Respon Request 2:", res2.status_code, res2.json())

if __name__ == "__main__":
    asyncio.run(main())