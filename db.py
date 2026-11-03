import sqlite3

def init_db():
    conn = sqlite3.connect('chess.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
         url TEXT PRIMARY KEY,
         time_class TEXT,
         my_colour TEXT,
         my_rating INTEGER,
         opponent_rating INTEGER,
         my_result TEXT,
         end_time INTEGER,
         opening TEXT)
     ''')
    return conn

def save_game(conn, game):
    conn.execute('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (game.url, game.time_class, game.my_colour, game.my_rating,
                   game.opponent_rating, game.my_result, game.end_time, game.opening))
    conn.commit()