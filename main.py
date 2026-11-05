from models import parse_game
from api import get_archives, get_games
from db import init_db, save_game
from stats import (results_summary, 
                   results_by_colour,
                   results_by_time_class, 
                   results_by_time_control, 
                   format_time_control,
                   results_by_opening,
                   results_by_hour,
                   format_hour,)
import time

username = 'Voolfenborg'
# archives = get_archives(username)

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
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    print(f'{colour:<6} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

print('\nBy time class:')
for time_class, total, wins, losses, draws in results_by_time_class(conn):
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    print(f'{time_class:<7} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

print('\nBy time control:')
for time_class, time_control, total, wins, losses, draws in results_by_time_control(conn):
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    label = f'{time_class} {format_time_control(time_control)}'
    print(f'{label:<14} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

print('\nTop openings:')
for opening, total, wins, losses, draws in results_by_opening(conn):
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    print(f'{opening:<46} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

print('\nBy hour:')
for hour, total, wins, losses, draws in results_by_hour(conn):
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    print(f'{format_hour(hour):>4} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')
