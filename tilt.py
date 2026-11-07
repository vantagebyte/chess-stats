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