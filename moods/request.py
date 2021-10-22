import sqlite3
import json
from models import Mood

def get_all_moods():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            mood.id,
            mood.label
        FROM Mood
        """)

    moods = []
    data = db_cursor.fetchall()
    for row in data:
        mood = Mood(row['id'], row['label'])
        moods.append(mood.__dict__)
    return json.dumps(moods)