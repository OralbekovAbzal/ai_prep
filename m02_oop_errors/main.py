from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)

class NotEnoughCredits(Exception):
    pass

@dataclass
class GenerationJob:
    prompt: str
    model: str
    duration_sec: int
    status: str = "queued"

    def cost(self):
        if self.model == "pro":
            return self.duration_sec * 5
        return self.duration_sec * 2
    def start(self):
        if self.status != "queued":
            raise ValueError("Статус не равен 'queued'")
        self.status = "running"

@dataclass
class Wallet:
    balance: int

    def charge(self,amount: int):
        if amount <= 0:
            raise ValueError("Amount of credits must be greater than 0")
        if self.balance - amount < 0:
            raise NotEnoughCredits(f"Нужно {amount}, на балансе {self.balance}")
        self.balance -= amount

def run_jobs(wallet: Wallet, jobs: list):
    for j in jobs:
        try:
            wallet.charge(j.cost())
            j.start()
        except NotEnoughCredits as e:
            logging.warning(f"Ошибка: {e}")
            continue

a = GenerationJob(prompt="Test", model="std", duration_sec=15)
w = Wallet(balance=30)

jobs = [a,a]
run_jobs(w,jobs)