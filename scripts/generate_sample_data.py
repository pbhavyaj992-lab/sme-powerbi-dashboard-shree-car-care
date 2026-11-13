#!/usr/bin/env python3
"""
Generate sample data for Shree Car Care, Anand.
Sample data only - fictional detailing centre, Jan-Jun 2026.

Run from anywhere:
    python3 scripts/generate_sample_data.py

Re-running overwrites the CSVs in data/ with the same rows,
because random.seed(42) is fixed.

Only Python stdlib is used: csv, random, datetime, pathlib.
No real personal data. Names, phones and amounts are made up.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- services
SERVICES = [
    # service_id, service name, category, price in INR, typical minutes
    ("S01", "Basic Wash", "Wash", 499, 45),
    ("S02", "Foam Wash + Vacuum", "Wash", 799, 60),
    ("S03", "Interior Detailing", "Detailing", 2499, 180),
    ("S04", "Ceramic Coating - 1 Year", "Coating", 9999, 360),
    ("S05", "Paint Protection - Single Panel", "Coating", 14999, 420),
    ("S06", "Engine Bay Cleaning", "Detailing", 999, 60),
    ("S07", "Headlight Restoration", "Detailing", 1299, 90),
    ("S08", "Bike Detailing", "Wash", 699, 60),
]

SERVICE_WEIGHTS = [28, 26, 14, 6, 2, 8, 6, 10]

STAFF = ["Arjun Patel", "Mehul Chauhan", "Jay Rathod", "Ravi Solanki", "Kiran Makwana"]

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Reyansh", "Krishna", "Ishaan",
    "Rohan", "Kabir", "Ananya", "Diya", "Aadhya", "Myra", "Sara", "Ira",
    "Priya", "Anika", "Navya", "Riya", "Aryan", "Dhruv", "Karan", "Manav",
    "Nikhil", "Sagar", "Hardik", "Jignesh", "Mahesh", "Ramesh", "Suresh",
    "Kiran", "Meera", "Nita", "Rekha", "Geeta", "Sunita", "Asha", "Lata",
    "Viral", "Parth", "Yash", "Dev", "Raj", "Amit", "Sanjay", "Vijay",
    "Hetal", "Kinjal", "Falguni", "Bhavik", "Chirag", "Nilesh", "Dipak",
    "Hiren", "Mitesh", "Prakash", "Anil", "Mukesh", "Rakesh",
]
LAST_NAMES = [
    "Patel", "Shah", "Desai", "Trivedi", "Mehta", "Chauhan", "Rathod",
    "Parmar", "Solanki", "Makwana", "Joshi", "Dave", "Bhatt", "Thakkar",
    "Prajapati", "Vaghela", "Chaudhary", "Gohil", "Zala", "Rabari",
]
CITIES = ["Anand", "Vallabh Vidyanagar", "Karamsad", "Borsad", "Nadiad", "Petlad"]
SOURCES = ["Walk-in", "Instagram", "Referral", "Google"]
SOURCE_WEIGHTS = [45, 25, 20, 10]

NOTES = [
    "custmer wanted foam wash only",
    "car was very durty after rain",
    "ceramik coating booked, custmer late by 30 min",
    "paymnt by UPI, screenshot saved",
    "custmer asked for extra vacuum",
    "two wheeler, light scratches",
    "regular custmer, gave 10% off on wash",
    "called before coming, slot 11 am",
    "custmer will come back next month",
    "interior was very dusty",
]


def write_csv(filename, fieldnames, rows):
    path = DATA / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} rows -> {path}")


def main():
    # ------------------------------------------------------------ customers
    customers = []
    used_names = set()
    i = 0
    while len(customers) < 185:
        i += 1
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        # Avoid exact duplicate names where possible.
        if name in used_names and i < 400:
            continue
        used_names.add(name)
        cid = f"C{len(customers) + 1:03d}"
        # 9 customers have no phone number - like a real walk-in sheet.
        if len(customers) in {12, 27, 44, 63, 81, 104, 126, 149, 171}:
            phone = ""
        else:
            phone = f"{random.choice(['9', '8', '7'])}{random.randint(100000000, 999999999)}"
        first_visit = date(2026, 1, 1) + timedelta(days=random.randint(0, 180))
        customers.append({
            "customer_id": cid,
            "customer_name": name,
            "phone": phone,
            "city": random.choice(CITIES),
            "source": random.choices(SOURCES, weights=SOURCE_WEIGHTS, k=1)[0],
            "first_visit_date": first_visit.isoformat(),
        })

    write_csv("sample_customers.csv",
              ["customer_id", "customer_name", "phone", "city", "source", "first_visit_date"],
              customers)

    # ------------------------------------------------------------- services
    service_rows = [{
        "service_id": sid,
        "service_name": name,
        "category": category,
        "price_inr": price,
        "duration_minutes": minutes,
    } for sid, name, category, price, minutes in SERVICES]
    write_csv("sample_services.csv",
              ["service_id", "service_name", "category", "price_inr", "duration_minutes"],
              service_rows)

    # ------------------------------------------------------------- bookings
    # 120 distinct open days inside Jan-Jun 2026.
    start = date(2026, 1, 1)
    all_days = [start + timedelta(days=d) for d in range(181)]  # 1 Jan - 30 Jun
    open_days = sorted(random.sample(all_days, 120))

    # Exactly 12 cancelled and 9 no-show, the rest completed.
    statuses = ["Completed"] * 299 + ["Cancelled"] * 12 + ["No-Show"] * 9
    random.shuffle(statuses)

    # Use every one of the 120 open days at least once, then fill the rest.
    booking_dates = list(open_days) + [
        random.choice(open_days) for _ in range(320 - len(open_days))
    ]
    random.shuffle(booking_dates)

    bookings = []
    for n in range(320):
        service = random.choices(SERVICES, weights=SERVICE_WEIGHTS, k=1)[0]
        status = statuses[n]
        amount = service[3] if status == "Completed" else 0
        payment = ""
        if status == "Completed":
            payment = random.choices(["UPI", "Cash", "Card"], weights=[45, 35, 20], k=1)[0]
        note = ""
        if random.random() < 0.12:
            note = random.choice(NOTES)
        bookings.append({
            "booking_id": f"B{n + 1:03d}",
            "booking_date": booking_dates[n].isoformat(),
            "customer_id": random.choice(customers)["customer_id"],
            "service_id": service[0],
            "staff_name": random.choice(STAFF),
            "channel": random.choices(SOURCES, weights=SOURCE_WEIGHTS, k=1)[0],
            "payment_method": payment,
            "status": status,
            "amount_inr": amount,
            "notes": note,
        })

    # Keep the file in date order so it reads like a real booking sheet.
    bookings.sort(key=lambda r: (r["booking_date"], r["booking_id"]))
    # Keep booking_id in date order too - renumber after sorting.
    for n, row in enumerate(bookings, start=1):
        row["booking_id"] = f"B{n:03d}"

    write_csv("sample_bookings.csv",
              ["booking_id", "booking_date", "customer_id", "service_id", "staff_name",
               "channel", "payment_method", "status", "amount_inr", "notes"],
              bookings)

    # ------------------------------------------------------------- expenses
    expense_rows = []
    exp_id = 1
    for month in range(1, 7):
        month_rows = [
            ("Rent - shop", "Rent", 18000),
            ("Staff salaries", "Salaries", 36000),
            ("Detailing chemicals", "Materials", random.randint(7500, 10500)),
            ("Cloths and consumables", "Materials", random.randint(1800, 3200)),
            ("Electricity bill", "Utilities", random.randint(3400, 5200)),
            ("Water bill", "Utilities", random.randint(700, 1200)),
            ("Instagram ads", "Marketing", random.randint(1500, 3500)),
            ("Equipment maintenance", "Maintenance", random.randint(800, 2500)),
            ("Miscellaneous", "Other", random.randint(500, 1800)),
        ]
        for description, category, amount in month_rows:
            expense_rows.append({
                "expense_id": f"E{exp_id:03d}",
                "expense_date": date(2026, month, random.randint(1, 28)).isoformat(),
                "category": category,
                "description": description,
                "amount_inr": amount,
                "payment_method": random.choices(["UPI", "Cash", "Bank Transfer"], weights=[50, 20, 30], k=1)[0],
            })
            exp_id += 1

    expense_rows.sort(key=lambda r: r["expense_date"])
    write_csv("sample_expenses.csv",
              ["expense_id", "expense_date", "category", "description", "amount_inr", "payment_method"],
              expense_rows)

    # ---------------------------------------------------------------- summary
    completed = [b for b in bookings if b["status"] == "Completed"]
    revenue = sum(b["amount_inr"] for b in completed)
    expenses_total = sum(r["amount_inr"] for r in expense_rows)
    print(f"Bookings: {len(bookings)} (Completed {len(completed)}, "
          f"Cancelled {sum(1 for b in bookings if b['status'] == 'Cancelled')}, "
          f"No-Show {sum(1 for b in bookings if b['status'] == 'No-Show')})")
    print(f"Total revenue (completed bookings): INR {revenue:,}")
    print(f"Total expenses: INR {expenses_total:,}")
    print(f"Net cash (revenue - expenses): INR {revenue - expenses_total:,}")
    print(f"Distinct booking dates: {len(set(b['booking_date'] for b in bookings))}")
    print(f"Customers with no phone: {sum(1 for c in customers if not c['phone'])}")


if __name__ == "__main__":
    main()
