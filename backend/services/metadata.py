import sqlite3
from typing import List, Optional

ROOT_DIR = "/home/shubhk/sentinal-ai"
DB_PATH = ROOT_DIR + "/.neocli/chroma/metadata.db"

class MetadataDB:
    def __init__(self, db_path=DB_PATH):
        print(f"[DB] Connecting to database at: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            print("[DB] Creating table and indexes if they don't exist...")
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    vector_id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    start_line INTEGER,
                    end_line INTEGER
                )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_file_path ON metadata(file_path)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_vector_id ON metadata(vector_id)")
            print("[DB] Table and indexes ready.")

    def add_chunk(self, vector_id: int, file_path: str, start: int, end: int):
        with self.conn:
            print(f"[DB] Adding chunk: ID={vector_id}, File={file_path}, Lines={start}-{end}")
            self.conn.execute("""
                INSERT OR REPLACE INTO metadata (vector_id, file_path, start_line, end_line)
                VALUES (?, ?, ?, ?)
            """, (vector_id, file_path, start, end))

    def remove_by_path(self, file_path: str):
        with self.conn:
            print(f"[DB] Removing chunks for file: {file_path}")
            self.conn.execute("DELETE FROM metadata WHERE file_path = ?", (file_path,))

    def get_vector_ids_by_path(self, file_path: str) -> List[int]:
        print(f"[DB] Fetching vector IDs for file: {file_path}")
        cur = self.conn.execute("SELECT vector_id FROM metadata WHERE file_path = ?", (file_path,))
        ids = [row[0] for row in cur.fetchall()]
        print(f"[DB] Found {len(ids)} vectors.")
        return ids
    def get_meta_for_vector_ids(self,vector_list):
        placeholders = ','.join(['?'] * len(vector_list))
        query = f"SELECT * FROM metadata WHERE vector_id IN ({placeholders})"
        print(query)
        print(vector_list.tolist())
        cur = self.conn.execute(query, vector_list.tolist())
        return cur.fetchall()
    def close(self):
        print("[DB] Closing connection.")
        self.conn.close()
