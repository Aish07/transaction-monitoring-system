import csv
from datetime import datetime
import random

# Users and merchants
users = [f"u{i}" for i in range(1, 9)]
merchants_regular = ["Starbucks", "Target", "Amazon", "Sephora", "Walmart", "McDonalds", "PizzaHut", "Subway", "Best Buy"]
merchants_luxury = ["Rolex Boutique", "Jewellery World"]
merchants_travel = ["Delta Airlines", "Booking.com", "Expedia", "Airbnb", "TripAdvisor", "Hilton Hotels"]

transactions = []

def random_time(start_date, hour_range=(0,23)):
    hour = random.randint(*hour_range)
    minute = random.randint(0,59)
    second = random.randint(0,59)
    return datetime(start_date.year, start_date.month, start_date.day, hour, minute, second)

for user in users:
    # Everyday purchases
    for _ in range(4):
        ts = random_time(datetime(2025, 1, random.randint(1,10)), hour_range=(7,20))
        merchant = random.choice(merchants_regular)
        amount = round(random.uniform(5, 350), 2)
        transactions.append([user, ts.strftime("%Y-%m-%d %H:%M:%S"), merchant, amount])
    
    # Fraud/high-value transactions
    if random.random() > 0.5:
        ts = random_time(datetime(2025, 2, random.randint(10,15)), hour_range=(1,3))
        merchant = random.choice(merchants_luxury)
        amount = random.choice([1500, 5000, 8000, 10000, 12000])
        transactions.append([user, ts.strftime("%Y-%m-%d %H:%M:%S"), merchant, amount])
    
    # Travel-related
    for _ in range(2):
        ts = random_time(datetime(2025, 3, random.randint(5,10)), hour_range=(8,16))
        merchant = random.choice(merchants_travel)
        amount = round(random.uniform(100, 800), 2)
        transactions.append([user, ts.strftime("%Y-%m-%d %H:%M:%S"), merchant, amount])

# Sort by timestamp
transactions.sort(key=lambda x: x[1])

# Write CSV
with open("data/input.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","timestamp","merchant_name","amount"])
    writer.writerows(transactions)

print("data/input.csv generated successfully!")
