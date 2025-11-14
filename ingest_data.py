import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'ecom.db'
CSV_FILES = {
    'products': BASE_DIR / 'products.csv',
    'customers': BASE_DIR / 'customers.csv',
    'orders': BASE_DIR / 'orders.csv',
    'order_items': BASE_DIR / 'order_items.csv',
    'categories': BASE_DIR / 'categories.csv',
}

CREATE_STATEMENTS = {
    'products': '''
        CREATE TABLE IF NOT EXISTS products (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Price REAL NOT NULL,
            Stock INTEGER NOT NULL
        );
    ''',
    'customers': '''
        CREATE TABLE IF NOT EXISTS customers (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Country TEXT NOT NULL
        );
    ''',
    'orders': '''
        CREATE TABLE IF NOT EXISTS orders (
            OrderID INTEGER PRIMARY KEY,
            CustomerID INTEGER NOT NULL,
            Date TEXT NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES customers(ID)
        );
    ''',
    'order_items': '''
        CREATE TABLE IF NOT EXISTS order_items (
            OrderID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
            FOREIGN KEY (ProductID) REFERENCES products(ID)
        );
    ''',
    'categories': '''
        CREATE TABLE IF NOT EXISTS categories (
            CategoryID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL
        );
    '''
}

INSERT_STATEMENTS = {
    'products': 'INSERT INTO products (ID, Name, Price, Stock) VALUES (?, ?, ?, ?)',
    'customers': 'INSERT INTO customers (ID, Name, Email, Country) VALUES (?, ?, ?, ?)',
    'orders': 'INSERT INTO orders (OrderID, CustomerID, Date) VALUES (?, ?, ?)',
    'order_items': 'INSERT INTO order_items (OrderID, ProductID, Quantity) VALUES (?, ?, ?)',
    'categories': 'INSERT INTO categories (CategoryID, Name) VALUES (?, ?)'
}

def load_products(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [(
            int(row['ID']),
            row['Name'],
            float(row['Price']),
            int(row['Stock'])
        ) for row in reader]

def load_customers(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [(
            int(row['ID']),
            row['Name'],
            row['Email'],
            row['Country']
        ) for row in reader]

def load_orders(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [(
            int(row['OrderID']),
            int(row['CustomerID']),
            row['Date']
        ) for row in reader]

def load_order_items(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [(
            int(row['OrderID']),
            int(row['ProductID']),
            int(row['Quantity'])
        ) for row in reader]

def load_categories(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [(
            int(row['CategoryID']),
            row['Name']
        ) for row in reader]

LOADERS = {
    'products': load_products,
    'customers': load_customers,
    'orders': load_orders,
    'order_items': load_order_items,
    'categories': load_categories,
}

def ensure_files_exist():
    missing = [name for name, path in CSV_FILES.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing CSV files: {', '.join(missing)}")

def main():
    ensure_files_exist()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        for table, statement in CREATE_STATEMENTS.items():
            cursor.execute(statement)
            cursor.execute(f'DELETE FROM {table}')

        for table, loader in LOADERS.items():
            rows = loader(CSV_FILES[table])
            cursor.executemany(INSERT_STATEMENTS[table], rows)

        conn.commit()
        print(f"Data ingested into {DB_PATH}")

if __name__ == '__main__':
    main()
