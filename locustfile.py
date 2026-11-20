from locust import HttpUser, task, between

class TokoBukuUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(2)
    def baca_buku(self):
        self.client.get("/resource?skip=0&limit=10")

    @task(1)
    def buat_transaksi(self):
        self.client.post("/transactions", json={"book_id": 2, "qty": 1})