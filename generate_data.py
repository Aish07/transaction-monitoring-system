import csv
from datetime import datetime, timedelta

# Users and merchants
users = [f"u{i}" for i in range(1, 9)]
merchants_regular = ["Starbucks", "Target", "Amazon", "Sephora", "Walmart", "McDonalds", "PizzaHut", "Subway", "Best Buy"]
merchants_luxury = ["Rolex Boutique", "Jewellery World"]
merchants_travel = ["Delta Airlines", "Booking.com", "Expedia", "Airbnb", "TripAdvisor", "Hilton Hotels"]

transactions = []

def add_transaction(user, ts, merchant, amount):
    transactions.append([user, ts.strftime("%Y-%m-%d %H:%M:%S"), merchant, amount])

# ---- Rule 2: Rapid small transactions (5 tx in 2 min) ----
base_time = datetime(2025, 1, 1, 10, 0, 0)
for i in range(5):
    add_transaction("u1", base_time + timedelta(seconds=i*20), "Starbucks", 10 + i)

# ---- Rule 3: Same merchant multiple times in 90s ----
base_time = datetime(2025, 1, 2, 11, 0, 0)
for i in range(3):
    add_transaction("u2", base_time + timedelta(seconds=i*30), "Walmart", 25)

# ---- Rule 4: Unusual time-of-day ----
# Normal hours for u3
for h in [9, 10, 11, 12]:
    add_transaction("u3", datetime(2025, 1, 3, h, 0, 0), "Target", 20)
# Unusual late night transaction
add_transaction("u3", datetime(2025, 1, 3, 3, 0, 0), "Amazon", 50)

# ---- Rule 5: Time-compressed spend spike ----
base_time = datetime(2025, 1, 4, 14, 0, 0)
add_transaction("u4", base_time, "Subway", 100)
add_transaction("u4", base_time + timedelta(minutes=10), "Subway", 150)
add_transaction("u4", base_time + timedelta(minutes=20), "Starbucks", 200)  # Spike total 450 in 20min

# ---- Rule 1: High-value transaction ----
add_transaction("u5", datetime(2025, 1, 5, 15, 0, 0), "Rolex Boutique", 8000)

# Fill some normal transactions for other users
base_time = datetime(2025, 1, 6, 9, 0, 0)
for u in ["u6", "u7", "u8"]:
    for h in range(8, 12):
        add_transaction(u, datetime(2025, 1, 6, h, 0, 0), "Walmart", 50)

# Sort by timestamp
transactions.sort(key=lambda x: x[1])

# Write CSV
with open("data/input.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id","timestamp","merchant_name","amount"])
    writer.writerows(transactions)

print("data/input.csv generated successfully!")
