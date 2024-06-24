import sqlite3
import os
from datetime import datetime

class DataStorage:
    def __init__(self, db_path='./../data/data.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS telemetry
                               (timestamp TEXT, humidity REAL)''')
        self.conn.commit()

    def store_data(self, humidity_value):
        timestamp = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO telemetry (timestamp, humidity) VALUES (?, ?)", (timestamp, humidity_value))
        self.conn.commit()

    def get_stored_data(self):
        self.cursor.execute("SELECT * FROM telemetry")
        rows = self.cursor.fetchall()
        return rows

    def delete_data(self, timestamp):
        self.cursor.execute("DELETE FROM telemetry WHERE timestamp = ?", (timestamp,))
        self.conn.commit()
