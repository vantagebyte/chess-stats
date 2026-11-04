def results_summary(conn):
    return conn.execute('SELECT my_result, COUNT(*) FROM games GROUP BY my_result').fetchall()

def results_by_colour(conn):
    return conn.execute('''
    SELECT my_colour,
       COUNT(*),
       SUM(my_result = 'win'),
       SUM(my_result = 'loss'),
       SUM(my_result = 'draw')
FROM games
GROUP BY my_colour
ORDER BY my_colour DESC''').fetchall()

def results_by_time_class(conn):
    return conn.execute('''SELECT time_class,
           COUNT(*),
           SUM(my_result = 'win'),
           SUM(my_result = 'loss'),
           SUM(my_result = 'draw')
    FROM games
    GROUP BY time_class
    ORDER BY COUNT(*) DESC''').fetchall()

def results_by_time_control(conn):
    return conn.execute('''SELECT time_class, time_control,
    COUNT(*),
    SUM(my_result = 'win'),
    SUM(my_result = 'loss'),
    SUM(my_result = 'draw')
FROM games
GROUP BY time_class, time_control
ORDER BY time_class, COUNT(*) DESC''').fetchall()

def format_time_control(tc):
    if tc == '-':
        return 'unknown'
    elif '/' in tc:
        seconds = int(tc.split('/')[1])
        days = seconds // 86400
        return f'{days} days'
    elif '+' in tc:
        base, increment = tc.split('+')
        minutes = int(base) // 60
        return f'{minutes}+{increment}'
    else:
        minutes = int(tc) // 60
        return f'{minutes} min'

        
    