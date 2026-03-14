import pymysql

# Configuration
db_host = "localhost"
db_user = "root"
db_pass = "ww22iixxzz"

try:
    # Connect to MySQL Server (without specifying a database)
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass)
    cursor = conn.cursor()
    
    # Create the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS smartmess;")
    print("✅ Database 'smartmess_db' created successfully!")
    
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}") 
