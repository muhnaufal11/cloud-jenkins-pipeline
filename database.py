import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'cloud_app.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insert initial sample record if empty
    cursor.execute('SELECT COUNT(*) FROM server_logs')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO server_logs (service_name, status) VALUES ('Jenkins-CI-Pipeline', 'Active')")
        cursor.execute("INSERT INTO server_logs (service_name, status) VALUES ('Docker-Engine-WSL2', 'Running')")
        cursor.execute("INSERT INTO server_logs (service_name, status) VALUES ('SQLite-Database', 'Connected')")
    conn.commit()
    conn.close()

def add_log(service_name, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO server_logs (service_name, status) VALUES (?, ?)", (service_name, status))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, service_name, status, created_at FROM server_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == '__main__':
    init_db()
    logs = get_all_logs()
    print(f"Database initialized with {len(logs)} records.")
