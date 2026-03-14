import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ww22iixxzz"
    )
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS smartmess")
    cursor.execute("CREATE DATABASE smartmess")
    print("Database 'smartmess' has been reset successfully.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error resetting database: {e}")
