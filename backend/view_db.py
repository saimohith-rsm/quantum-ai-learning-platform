"""
Quick Interactive & Terminal Viewer for quantum_learning.db
Run: python view_db.py [table_name]
"""
import sys
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantum_learning.db")

def show_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    print("\n" + "=" * 60)
    print("  📊 DATABASE: quantum_learning.db")
    print("=" * 60)
    for table in tables:
        count = cursor.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"  • {table:<25} ({count} rows)")
    print("=" * 60 + "\n")
    return tables

def show_table_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 20;")
    rows = cursor.fetchall()
    
    print(f"\n--- Table: {table_name} (Showing up to 20 rows) ---")
    if not rows:
        print("  (Empty table)")
        return
    
    # Print headers
    header = " | ".join(f"{col:<15}" for col in columns[:8])
    print(header)
    print("-" * len(header))
    for row in rows:
        row_str = " | ".join(f"{str(row[col])[:15]:<15}" for col in columns[:8])
        print(row_str)
    print()

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        
    tables = show_tables()
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        if target in tables:
            show_table_data(target)
        else:
            print(f"Table '{target}' not found.")
    else:
        for t in tables:
            show_table_data(t)
