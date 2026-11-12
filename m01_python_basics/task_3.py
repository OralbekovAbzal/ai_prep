from collections import defaultdict

def diferent_cities(tx: list) -> defaultdict:
    cards = defaultdict(set)
    for t in tx:
        cards[t["card"]].add(t["city"])

    counts = defaultdict(int)
    for card, citites in cards.items():
        l = len(citites)
        if l == 1:
            continue
        counts[card] = l
    return counts

def total_amount_count(tx: list) -> defaultdict:
    amount = defaultdict(int)
    count = defaultdict(int)

    for t in tx:
        amount[t["card"]] += t["amount"]
        count[t["card"]] += 1
    return amount, count

#Изменение списка транзакций может сломать проверки через assert
transactions = [
    {"card": "…1234", "amount": 15000, "city": "Астана"},
    {"card": "…5678", "amount": 70000, "city": "Алматы"},
    {"card": "…9012", "amount": 1200, "city": "Шымкент"},
    {"card": "…3456", "amount": 45000, "city": "Караганда"},
    {"card": "…1234", "amount": 2300, "city": "Астана"},
    {"card": "…7890", "amount": 18000, "city": "Астана"},
    {"card": "…9012", "amount": 250000, "city": "Дубай"},
    {"card": "…3456", "amount": 7000, "city": "Караганда"},
    {"card": "…5678", "amount": 3500, "city": "Алматы"},
    {"card": "…1234", "amount": 87000, "city": "Алматы"},
    {"card": "…7890", "amount": 22000, "city": "Павлодар"},
    {"card": "…9012", "amount": 5600, "city": "Шымкент"},
    {"card": "…3456", "amount": 8200, "city": "Караганда"},
    {"card": "…1234", "amount": 4500, "city": "Астана"},
    {"card": "…5678", "amount": 9800, "city": "Алматы"},
    {"card": "…7890", "amount": 6400, "city": "Астана"},
    {"card": "…9012", "amount": 300000, "city": "Стамбул"},
    {"card": "…3456", "amount": 3300, "city": "Караганда"},
    {"card": "…1234", "amount": 12000, "city": "Астана"},
    {"card": "…7890", "amount": 9900, "city": "Астана"},
]

assert diferent_cities(transactions) == {'…1234': 2, '…9012': 3, '…7890': 2}
assert total_amount_count(transactions) == (({'…1234': 120800, '…5678': 83300, '…9012': 556800, '…3456': 63500, '…7890': 56300}), ( {'…1234': 5, '…5678': 3, '…9012': 4, '…3456': 4, '…7890': 4}))
assert diferent_cities([]) == {}
assert total_amount_count([]) == ({},{})