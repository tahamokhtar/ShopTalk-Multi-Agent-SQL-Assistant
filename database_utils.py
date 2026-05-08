import sqlite3

def get_db_connection():
    # الاتصال بملف قاعدة البيانات
    return sqlite3.connect('shoptalk.db')

def get_db_schema():
    """استخراج هيكل قاعدة البيانات لتقديمه للـ LLM"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # استخراج أسماء الجداول في SQLite
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_description = []
    
    for (table_name,) in tables:
        # استخراج تفاصيل الأعمدة لكل جدول
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # معلومات العمود في SQLite تكون في الفهرس 1 (الاسم) و 2 (النوع)
        col_desc = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema_description.append(f"Table: {table_name}\nColumns: {col_desc}")
    
    conn.close()
    return "\n\n".join(schema_description)

# تجربة الكود للتأكد أنه يعمل
if __name__ == "__main__":
    print("--- Database Schema Detected ---")
    print(get_db_schema())