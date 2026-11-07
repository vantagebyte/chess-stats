from models import (parse_game,
                    get_start_time,)
from api import get_archives, get_games
from db import init_db, save_game
from stats import (results_summary, 
                   results_by_colour,
                   results_by_time_class, 
                   results_by_time_control, 
                   format_time_control,
                   results_by_opening,
                   results_by_hour,
                   format_hour,
                  )
from tilt import (load_games, 
                  split_sittings, 
                  results_after,
                  results_by_streak,
                  results_by_game_number,
                  longest_streaks,)
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


games = load_games(conn)
sittings = split_sittings(games)
counts = results_after(sittings)
print('\nTilt: result after...')
for prev, outcomes in counts.items():
    wins = outcomes['win']
    losses = outcomes['loss']
    draws = outcomes['draw']
    total = wins + losses + draws
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    label = f'After a {prev}'
    print(f'{label:<12} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

streaks = results_by_streak(sittings)

print('\nTilt: result after a streak...')
PLURALS = {'win': 'wins', 'loss': 'losses'}
for (streak_result, n), outcomes in sorted(streaks.items()):
    wins = outcomes['win']
    losses = outcomes['loss']
    draws = outcomes['draw']
    total = wins + losses + draws
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    length = '3+' if n == 3 else str(n)
    word = streak_result if n == 1 else PLURALS[streak_result]
    label = f'After {length} {word}'
    print(f'{label:<15} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')
    
    by_number = results_by_game_number(sittings)

print('\nTilt: result by game number in a sitting...')
for n, outcomes in sorted(by_number.items()):
    wins = outcomes['win']
    losses = outcomes['loss']
    draws = outcomes['draw']
    total = wins + losses + draws
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    length = '6+' if n == 6 else str(n)
    label = f'Game {length}'
    print(f'{label:<7} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')
    
    best = longest_streaks(sittings)

print('\nLongest streaks (in one sitting):')
print(f"Wins:    {best['win']}")
print(f"Losses:  {best['loss']}")
print(f"Winless: {best['winless']}")