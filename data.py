import sqlite3
import random
from datetime import datetime, timedelta

# الاتصال بقاعدة البيانات (سيتم إنشاؤها إذا لم توجد)
conn = sqlite3.connect('shoptalk.db')
cursor = conn.cursor()

print("1. Checking and creating tables...")

# إنشاء الجداول
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock_quantity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sale_date TEXT,
    quantity INTEGER,
    total_amount REAL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

# مسح البيانات القديمة لضمان عدم التكرار
cursor.execute('DELETE FROM sales')
cursor.execute('DELETE FROM products')

print("2. Generating 50 products and 5000 sales transactions...")

# توليد 50 منتج
categories = ['Electronics', 'Accessories', 'Furniture', 'Clothing', 'Books']
products_list = []
for i in range(1, 51):
    cat = random.choice(categories)
    price = round(random.uniform(20.0, 1500.0), 2)
    products_list.append((i, f"{cat} Item {i}", cat, price, random.randint(5, 100)))

cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', products_list)

# توليد 5000 عملية بيع خلال الـ 6 أشهر الماضية
sales_list = []
start_date = datetime.now() - timedelta(days=180)

for i in range(1, 5001):
    p_id = random.randint(1, 50)
    p_price = next(p[3] for p in products_list if p[0] == p_id)
    
    # تاريخ عشوائي
    r_days = random.randint(0, 180)
    s_date = (start_date + timedelta(days=r_days)).strftime('%Y-%m-%d')
    
    qty = random.randint(1, 5)
    total = round(qty * p_price, 2)
    sales_list.append((i, p_id, s_date, qty, total))

cursor.executemany('INSERT INTO sales VALUES (?,?,?,?,?)', sales_list)

conn.commit()
conn.close()

print("✅ Success! Database 'shoptalk.db' is ready with 5000 records.")