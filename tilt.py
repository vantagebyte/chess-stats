BREAK_SECONDS = 10 * 60

def load_games(conn):
    return conn.execute('''
    SELECT start_time, end_time, my_result
    FROM games
    WHERE time_class != 'daily'
    ORDER BY start_time
    ''').fetchall()

def split_sittings(games):
    sittings = []
    current = []
    prev_end = None
    for start, end, result in games:
        if prev_end is not None and start - prev_end > BREAK_SECONDS:
            sittings.append(current)
            current = []
        current.append(result)
        prev_end = end
    sittings.append(current)
    return sittings

def results_after(sittings):
    counts = {
        'win':  {'win': 0, 'loss': 0, 'draw': 0},
        'loss': {'win': 0, 'loss': 0, 'draw': 0},
        'draw': {'win': 0, 'loss': 0, 'draw': 0},
        }
    for sitting in sittings:
        prev = None
        for result in sitting:
            if prev is not None:
                counts[prev][result] += 1
            prev = result
    return counts

def results_by_streak(sittings):
    counts = {}
    for sitting in sittings:
        streak_result = None
        streak_len = 0
        for result in sitting:
            if streak_result in ('win', 'loss'):
                key = (streak_result, min(streak_len, 3))
                if key not in counts:
                    counts[key] = {'win': 0, 'loss': 0, 'draw': 0}
                counts[key][result] += 1
            if result == streak_result:
                streak_len += 1
            else:
                streak_result = result
                streak_len = 1
    return counts

def results_by_game_number(sittings):
    counts = {}
    for sitting in sittings:
        for number, result in enumerate(sitting, 1):
            key = min(number, 6)
            if key not in counts:
                counts[key] = {'win': 0, 'loss': 0, 'draw': 0}
            counts[key][result] += 1
    return counts

def longest_streaks(sittings):
    best = {'win': 0, 'loss': 0, 'winless': 0}
    for sitting in sittings:
        win_run = 0
        loss_run = 0
        winless_run = 0
        for result in sitting:
            if result == 'win':
                win_run += 1
                loss_run = 0
                winless_run = 0
            elif result == 'loss':
                win_run = 0
                loss_run += 1
                winless_run += 1
                
            else:
                win_run = 0
                loss_run = 0
                winless_run += 1
            best['win'] = max(best['win'], win_run)
            best['loss'] = max(best['loss'], loss_run)
            best['winless'] = max(best['winless'], winless_run)
    return best