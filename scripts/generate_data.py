from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
out = Path("data")
out.mkdir(exist_ok=True)

products = []
for i, (cat, sub) in enumerate([
    ("Electronics", "Mobile"), ("Electronics", "Laptop"), ("Home", "Kitchen"), ("Home", "Furniture"),
    ("Fashion", "Men"), ("Fashion", "Women"), ("Sports", "Fitness"), ("Beauty", "Skincare"),
], start=1):
    products.append({"product_id": f"P{i:03}", "product_name": f"{sub} {i}", "category": cat, "subcategory": sub, "price": round(random.uniform(20, 1200), 2)})

regions = [
    {"region_id": "R1", "region_name": "North America", "market": "AMER"},
    {"region_id": "R2", "region_name": "Europe", "market": "EMEA"},
    {"region_id": "R3", "region_name": "Asia Pacific", "market": "APAC"},
    {"region_id": "R4", "region_name": "Latin America", "market": "LATAM"},
]

customers = []
segments = ["SMB", "Mid-Market", "Enterprise", "Consumer"]
for i in range(1, 121):
    customers.append({
        "customer_id": f"C{i:04}",
        "segment": random.choice(segments),
        "country": random.choice(["US", "UK", "DE", "IN", "BR", "CA", "AU"]),
        "signup_date": (date(2023, 1, 1) + timedelta(days=random.randint(0, 700))).isoformat(),
        "churned": random.random() < 0.18,
    })

sales = []
start = date(2024, 1, 1)
for i in range(1, 1201):
    d = start + timedelta(days=random.randint(0, 730))
    p = random.choice(products)
    qty = random.randint(1, 9)
    base = p["price"] * qty
    revenue = round(base * random.uniform(0.9, 1.15), 2)
    cost = round(revenue * random.uniform(0.55, 0.82), 2)
    sales.append({
        "order_id": f"O{i:06}", "order_date": d.isoformat(), "product_id": p["product_id"],
        "region_id": random.choice(regions)["region_id"], "customer_id": random.choice(customers)["customer_id"],
        "revenue": revenue, "quantity": qty, "cost": cost,
    })

churn = []
for year in [2024, 2025]:
    for month in range(1, 13):
        ym = f"{year}-{month:02}"
        for seg in segments:
            churn.append({
                "month": ym,
                "segment": seg,
                "churn_rate": round(random.uniform(0.02, 0.15), 4),
                "retained_customers": random.randint(1200, 5000),
            })

def dump(name: str, rows: list[dict]) -> None:
    with (out / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

dump("sales.csv", sales)
dump("products.csv", products)
dump("customers.csv", customers)
dump("regions.csv", regions)
dump("churn.csv", churn)
print("generated")
