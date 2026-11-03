from models import parse_game
from api import get_archives, get_games
from db import init_db, save_game
from stats import results_summary

username = 'Voolfenborg'
archives = get_archives(username)
last_month = archives[-2]
games = get_games(last_month)

conn = init_db()
for game in games:
    save_game(conn, parse_game(game, username))
count = conn.execute('SELECT COUNT(*) FROM games').fetchone()
print(f'Games in database: {count[0]}')
rows = results_summary(conn)
total = count[0]
for result, n in rows:
    print(f'{result}: {n} ({n / total * 100:.1f}%)')
