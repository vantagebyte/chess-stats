import sqlite3

def init_db():
    conn = sqlite3.connect('chess.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
         url TEXT PRIMARY KEY,
         time_class TEXT,
         time_control TEXT,
         my_colour TEXT,
         my_rating INTEGER,
         opponent_rating INTEGER,
         my_result TEXT,
         start_time INTEGER,
         end_time INTEGER,
         opening TEXT)
     ''')
    return conn

def save_game(conn, game):
    conn.execute('INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (game.url, game.time_class, game.time_control, game.my_colour, game.my_rating,
                   game.opponent_rating, game.my_result, game.start_time, game.end_time, game.opening))
    conn.commit()