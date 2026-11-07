from models import parse_game
from api import get_archives, get_games
from db import init_db, save_game
from stats import (results_summary,
                   results_by_colour,
                   results_by_time_class,
                   results_by_time_control,
                   results_by_opening,
                   results_by_hour,
                   filtered_results,)
from tilt import (load_games,
                  split_sittings,
                  results_after,
                  results_by_streak,
                  results_by_game_number,
                  longest_streaks,)
from display import (format_time_control,
                     format_hour,
                     print_row,
                     print_filtered,)
from datetime import datetime, timezone
import time

username = 'Voolfenborg'
conn = init_db()

def update_games(conn):
    before = conn.execute('SELECT COUNT(*) FROM games').fetchone()[0]
    newest = conn.execute('SELECT MAX(end_time) FROM games').fetchone()[0]
    start_month = datetime.fromtimestamp(newest, timezone.utc).strftime('%Y/%m')
    archives = get_archives(username)
    for month_url in archives:
        if month_url[-7:] < start_month:
            continue
        games = get_games(month_url)
        print(f'{month_url}: {len(games)} games')
        for game in games:
            save_game(conn, parse_game(game, username))
        time.sleep(1)
    after = conn.execute('SELECT COUNT(*) FROM games').fetchone()[0]
    print(f'{after - before} new games added')
        
def ask(question):
    answer = input(question).strip().lower()
    if answer == '':
        return None
    return answer        

def show_overview(conn):
    count = conn.execute('SELECT COUNT(*) FROM games').fetchone()
    print(f'Games in database: {count[0]}')
    rows = results_summary(conn)
    total = count[0]
    for result, n in rows:
        print(f'{result}: {n} ({n / total * 100:.1f}%)')

    print('\nBy colour:')
    for colour, total, wins, losses, draws in results_by_colour(conn):
        print_row(colour, total, wins, losses, draws, 6)

    print('\nBy time class:')
    for time_class, total, wins, losses, draws in results_by_time_class(conn):
        print_row(time_class, total, wins, losses, draws, 7)

    print('\nBy time control:')
    for time_class, time_control, total, wins, losses, draws in results_by_time_control(conn):
        label = f'{time_class} {format_time_control(time_control)}'
        print_row(label, total, wins, losses, draws, 14)

    print('\nTop openings:')
    for opening, total, wins, losses, draws in results_by_opening(conn):
        print_row(opening, total, wins, losses, draws, 46)

    print('\nBy hour:')
    for hour, total, wins, losses, draws in results_by_hour(conn):
        print_row(f'{format_hour(hour):>4}', total, wins, losses, draws, 4)


def show_tilt(conn):
    games = load_games(conn)
    sittings = split_sittings(games)
    print('\nTilt: result after...')
    for prev, outcomes in results_after(sittings).items():
        label = f'After a {prev}'
        total = sum(outcomes.values())
        print_row(label, total, outcomes['win'], outcomes['loss'], outcomes['draw'], 12)

    print('\nTilt: result after a streak...')
    PLURALS = {'win': 'wins', 'loss': 'losses'}
    for (streak_result, n), outcomes in sorted(results_by_streak(sittings).items()):
        length = '3+' if n == 3 else str(n)
        word = streak_result if n == 1 else PLURALS[streak_result]
        label = f'After {length} {word}'
        total = sum(outcomes.values())
        print_row(label, total, outcomes['win'], outcomes['loss'], outcomes['draw'], 15)

    print('\nTilt: result by game number in a sitting...')
    for n, outcomes in sorted(results_by_game_number(sittings).items()):
        length = '6+' if n == 6 else str(n)
        label = f'Game {length}'
        total = sum(outcomes.values())
        print_row(label, total, outcomes['win'], outcomes['loss'], outcomes['draw'], 7)

    best = longest_streaks(sittings)
    print('\nLongest streaks (in one sitting):')
    print(f"Wins:    {best['win']}")
    print(f"Losses:  {best['loss']}")
    print(f"Winless: {best['winless']}")
    
def show_filtered(conn):
    colour = ask('Colour (white/black, Enter to skip): ')
    time_class = ask('Time class (bullet/blitz/rapid, Enter to skip): ')
    opening = ask('Opening (part of the name, Enter to skip): ')
    row = filtered_results(conn, colour=colour, time_class=time_class, opening=opening)
    print()
    print_filtered('Result', row)
        

while True:
    print(f'\nChess Stats — {username}')
    print('1. Update games')
    print('2. Overview stats')
    print('3. Tilt stats')
    print('4. Filter stats')
    print('0. Quit')
    choice = input('Choose: ')

    if choice == '1':
        update_games(conn)
    elif choice == '2':
        show_overview(conn)
    elif choice == '3':
        show_tilt(conn)
    elif choice == '4':
        show_filtered(conn)
    elif choice == '0':
        break
    else:
        print('Not an option, try again.')