"""
Interactive Terminal Viewer for MongoDB database (quantum_learning)
Run: python view_db.py [collection_name]
"""
import sys
import os
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "quantum_learning")

def get_mongo_db():
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=3000)
    return client[MONGODB_DB_NAME]

def show_collections():
    db = get_mongo_db()
    collections = sorted(db.list_collection_names())
    print("\n" + "=" * 60)
    print(f"  🍃 MONGODB DATABASE: {MONGODB_DB_NAME}")
    print(f"  🔗 URI: {MONGODB_URI}")
    print("=" * 60)
    for col_name in collections:
        count = db[col_name].count_documents({})
        print(f"  • {col_name:<25} ({count} documents)")
    print("=" * 60 + "\n")
    return collections

def show_collection_data(col_name):
    db = get_mongo_db()
    docs = list(db[col_name].find({}, {"_id": 0}).limit(10))
    
    print(f"\n--- Collection: {col_name} (Showing up to 10 documents) ---")
    if not docs:
        print("  (Empty collection)")
        return

    # Extract all keys present in sample documents
    all_keys = []
    for d in docs:
        for k in d.keys():
            if k not in all_keys:
                all_keys.append(k)

    header = " | ".join(f"{k:<15}" for k in all_keys[:6])
    print(header)
    print("-" * len(header))
    for d in docs:
        row_str = " | ".join(f"{str(d.get(k, ''))[:15]:<15}" for k in all_keys[:6])
        print(row_str)
    print()

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        collections = show_collections()
        target = sys.argv[1] if len(sys.argv) > 1 else None
        if target:
            if target in collections:
                show_collection_data(target)
            else:
                print(f"Collection '{target}' not found.")
        else:
            for c in collections:
                show_collection_data(c)
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")

