from models import parse_game
from api import get_archives, get_games
from db import init_db, save_game
from stats import results_summary
import time

username = 'Voolfenborg'
archives = get_archives(username)

conn = init_db()
for month_url in archives:
    games = get_games(month_url)
    print(f'{month_url}: {len(games)} games')
    for game in games:
        save_game(conn, parse_game(game, username))
    time.sleep(1)
count = conn.execute('SELECT COUNT(*) FROM games').fetchone()
print(f'Games in database: {count[0]}')
rows = results_summary(conn)
total = count[0]
for result, n in rows:
    print(f'{result}: {n} ({n / total * 100:.1f}%)')
