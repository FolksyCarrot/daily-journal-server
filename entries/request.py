import sqlite3
import json
from models import Entries
from models import Mood

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            Entries.id,
            Entries.concept,
            Entries.entry,
            Entries.mood_id,
            Mood.id,
            Mood.label
        FROM Entries
        JOIN Mood
        ON Entries.mood_id = Mood.id
        """)

        entrie = []
        data = db_cursor.fetchall()
        for row in data:
            entry = Entries(row['id'], row['concept'], row['entry'], row['mood_id'])
            entry.moods = Mood(row['id'], row['label']).__dict__
            entrie.append(entry.__dict__)

        return json.dumps(entrie)  

def get_single_entries(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            Entries.id,
            Entries.concept,
            Entries.entry,
            Entries.mood_id
        FROM Entries
        WHERE entries.id = ?
        """, (id,)) 
        data = db_cursor.fetchone()
        
        entries = Entries(data['id'], data['concept'], data['entry'], data['mood_id'])
        return json.dumps(entries.__dict__)

def delete_entry(id):
   with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Entries
        WHERE Entries.id = ?
        """,(id,)) 

def search_all_entries(searchTerm):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(f"""
        SELECT
            Entries.id,
            Entries.concept,
            Entries.entry,
            Entries.mood_id
        FROM Entries
        WHERE Entries.entry LIKE "%{searchTerm}%"
        """)

        entrie = []
        data = db_cursor.fetchall()
        for row in data:
            entry = Entries(row['id'], row['concept'], row['entry'], row['mood_id']).__dict__
            entrie.append(entry)
        return json.dumps(entrie)  