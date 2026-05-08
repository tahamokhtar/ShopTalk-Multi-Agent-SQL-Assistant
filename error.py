def execute_and_refine(query, question):
    import sqlite3
    conn = sqlite3.connect('shoptalk.db')
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return {"status": "success", "data": results}
    except Exception as e:
        # هنا تحدث عملية الـ Self-Correction (إعادة المحاولة)
        return {"status": "error", "message": str(e)}