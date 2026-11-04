from models import parse_game
from api import get_archives, get_games
from db import init_db, save_game
from stats import results_summary, results_by_colour, results_by_time_class
import time

username = 'Voolfenborg'
archives = get_archives(username)

conn = init_db()
# for month_url in archives:
#     games = get_games(month_url)
#     print(f'{month_url}: {len(games)} games')
#     for game in games:
#         save_game(conn, parse_game(game, username))
#     time.sleep(1)
count = conn.execute('SELECT COUNT(*) FROM games').fetchone()
print(f'Games in database: {count[0]}')
rows = results_summary(conn)
total = count[0]
for result, n in rows:
    print(f'{result}: {n} ({n / total * 100:.1f}%)')
print('\nBy colour:')
for colour, total, wins, losses, draws in results_by_colour(conn):
    print(f'{colour}: {total} games | {wins / total * 100:.1f}% W | {losses / total * 100:.1f}% L | {draws / total * 100:.1f}% D')

print('\nBy time class:')
for time_class, total, wins, losses, draws in results_by_time_class(conn): 
    print(f'{time_class}: {total} games | {wins / total * 100:.1f}% W | {losses / total * 100:.1f}% L | {draws / total * 100:.1f}% D')