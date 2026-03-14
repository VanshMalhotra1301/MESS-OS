import pymysql

# Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "ww22iixxzz"
DB_NAME = "smartmess"

def fix_expiry_column():
    print(f"🔧 Connecting to MySQL database: {DB_NAME}...")
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = conn.cursor()
        
        print("\nFixing 'surplus_posts' table...")
        # Increase the size of the column to hold full timestamps
        cursor.execute("ALTER TABLE surplus_posts MODIFY expiry_time VARCHAR(100)")
        print("  ✅ Column 'expiry_time' expanded to VARCHAR(100).")
        
        conn.commit()
        conn.close()
        print("\n🎉 Database repair complete! Try broadcasting again.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    fix_expiry_column()