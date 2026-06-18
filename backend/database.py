import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "ecommerce.db"

CUSTOMERS = [
    ("Alice Rossi", "alice@email.com", "Italy"),
    ("Marco Bianchi", "marco@email.com", "Italy"),
    ("James Smith", "james@email.com", "UK"),
    ("Fatima Al-Hassan", "fatima@email.com", "UAE"),
    ("Yuki Tanaka", "yuki@email.com", "Japan"),
    ("Carlos Rivera", "carlos@email.com", "Spain"),
    ("Emma Müller", "emma@email.com", "Germany"),
    ("Liam O'Brien", "liam@email.com", "Ireland"),
    ("Sofia Petrov", "sofia@email.com", "Russia"),
    ("Omar Khalid", "omar@email.com", "Saudi Arabia"),
    ("Chen Wei", "chen@email.com", "China"),
    ("Ana Lima", "ana@email.com", "Brazil"),
    ("David Cohen", "david@email.com", "Israel"),
    ("Priya Sharma", "priya@email.com", "India"),
    ("Noah Williams", "noah@email.com", "USA"),
]

PRODUCTS = [
    ("Wireless Headphones Pro", "Electronics", 149.99, 80),
    ("Mechanical Keyboard", "Electronics", 89.99, 120),
    ("Ergonomic Mouse", "Electronics", 59.99, 200),
    ("4K Webcam", "Electronics", 119.99, 60),
    ("USB-C Hub 7-in-1", "Electronics", 49.99, 150),
    ("Standing Desk Mat", "Office", 39.99, 90),
    ("Monitor Stand", "Office", 34.99, 110),
    ("Laptop Sleeve 15\"", "Accessories", 24.99, 250),
    ("Cable Management Kit", "Office", 14.99, 300),
    ("Noise Cancelling Earbuds", "Electronics", 79.99, 95),
    ("Blue Light Glasses", "Accessories", 29.99, 180),
    ("Portable SSD 1TB", "Electronics", 99.99, 70),
    ("Smart LED Desk Lamp", "Office", 44.99, 130),
    ("Wrist Rest Pad", "Office", 19.99, 220),
    ("Phone Stand Adjustable", "Accessories", 17.99, 260),
]

STATUSES = ["completed", "completed", "completed", "pending", "cancelled"]


def seed_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            country TEXT NOT NULL,
            joined_date TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    base_date = datetime(2023, 1, 1)
    for i, (name, email, country) in enumerate(CUSTOMERS):
        joined = base_date + timedelta(days=random.randint(0, 365))
        c.execute(
            "INSERT INTO customers (name, email, country, joined_date) VALUES (?, ?, ?, ?)",
            (name, email, country, joined.strftime("%Y-%m-%d")),
        )

    for name, category, price, stock in PRODUCTS:
        c.execute(
            "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
            (name, category, price, stock),
        )

    order_id = 1
    for customer_id in range(1, len(CUSTOMERS) + 1):
        num_orders = random.randint(2, 6)
        for _ in range(num_orders):
            order_date = base_date + timedelta(days=random.randint(0, 540))
            status = random.choice(STATUSES)
            num_items = random.randint(1, 4)
            products_chosen = random.sample(
                range(1, len(PRODUCTS) + 1), num_items)

            total = 0.0
            items = []
            for prod_id in products_chosen:
                qty = random.randint(1, 3)
                price = PRODUCTS[prod_id - 1][2]
                total += qty * price
                items.append((prod_id, qty, price))

            c.execute(
                "INSERT INTO orders (customer_id, order_date, status, total) VALUES (?, ?, ?, ?)",
                (customer_id, order_date.strftime(
                    "%Y-%m-%d"), status, round(total, 2)),
            )

            for prod_id, qty, price in items:
                c.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, prod_id, qty, price),
                )
            order_id += 1

    conn.commit()
    conn.close()
    print(f"✅ Database seeded at {DB_PATH}")


if __name__ == "__main__":
    seed_database()
