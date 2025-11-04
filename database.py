import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            time TEXT NOT NULL,
            timestamp DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            time TEXT NOT NULL,
            timestamp DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_score(username, score, time):
    conn = sqlite3.connect('data.db')
    conn.execute('INSERT INTO history (username, score, time) VALUES (?, ?, ?)', (username, score, time))
    conn.commit()
    conn.close()
    refresh_leaderboard()
    
def refresh_leaderboard():
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM leaderboard')
    cursor = conn.execute('SELECT username, score, time FROM history ORDER BY score DESC LIMIT 10')
    top_scores = cursor.fetchall()
    for entry in top_scores:
        conn.execute('INSERT INTO leaderboard (username, score, time) VALUES (?, ?, ?)', entry)
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT username, score, time FROM leaderboard ORDER BY score DESC')
    rows = cursor.fetchall()
    leaderboard = [{'username': row[0], 'score': row[1], 'time': row[2]} for row in rows]
    conn.close()
    return leaderboard

