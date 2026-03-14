import pymysql

# Configuration (Your Database Credentials)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "ww22iixxzz"
DB_NAME = "smartmess"

def fix_database_tables():
    print(f"🔧 Connecting to MySQL database: {DB_NAME}...")
    
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = conn.cursor()
        
        # --- 1. Fix 'surplus_posts' Table ---
        print("\nChecking 'surplus_posts' table...")
        cursor.execute("DESCRIBE surplus_posts")
        columns = [row[0] for row in cursor.fetchall()]
        
        if 'claimed_by_ngo_id' not in columns:
            print("  ⚠️ Missing column 'claimed_by_ngo_id'. Adding it now...")
            cursor.execute("ALTER TABLE surplus_posts ADD COLUMN claimed_by_ngo_id INT DEFAULT NULL")
            print("  ✅ Fixed.")
        else:
            print("  ✅ Table is already up to date.")

        # --- 2. Fix 'attendance_records' Table ---
        print("\nChecking 'attendance_records' table...")
        cursor.execute("DESCRIBE attendance_records")
        att_columns = [row[0] for row in cursor.fetchall()]
        
        # Columns needed for real logging
        needed_cols = {
            'prepared_qty': 'FLOAT DEFAULT 0.0',
            'consumed_qty': 'FLOAT DEFAULT 0.0',
            'wasted_qty': 'FLOAT DEFAULT 0.0',
            'actual_attendance': 'INT DEFAULT 0'
        }
        
        for col_name, col_def in needed_cols.items():
            if col_name not in att_columns:
                print(f"  ⚠️ Missing column '{col_name}'. Adding it...")
                cursor.execute(f"ALTER TABLE attendance_records ADD COLUMN {col_name} {col_def}")
                print(f"  ✅ Fixed.")
        
        print("\n🎉 Database repair complete! Your project is now synchronized.")
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"\n❌ Error connecting to database: {e}")
        print("Make sure your MySQL server is running and the password is correct.")

if __name__ == "__main__":
    fix_database_tables()