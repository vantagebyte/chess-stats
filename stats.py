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

def results_by_opening(conn):
    return conn.execute('''SELECT opening,
           COUNT(*),
           SUM(my_result = 'win'),
           SUM(my_result = 'loss'),
           SUM(my_result = 'draw')
    FROM games
    GROUP BY opening
    ORDER BY COUNT(*) DESC
    LIMIT 10''').fetchall()

def results_by_time_control(conn):
    return conn.execute('''SELECT time_class, time_control,
    COUNT(*),
    SUM(my_result = 'win'),
    SUM(my_result = 'loss'),
    SUM(my_result = 'draw')
FROM games
GROUP BY time_class, time_control
ORDER BY time_class, COUNT(*) DESC''').fetchall()

def results_by_hour(conn):
    return conn.execute('''SELECT
               strftime('%H', end_time, 'unixepoch', 'localtime')
               As hour, COUNT(*),
               SUM(my_result = 'win'),
               SUM(my_result = 'loss'),
               SUM(my_result = 'draw')
        FROM games       
        GROUP BY hour
        ORDER BY hour
        ''').fetchall()

def filtered_results(conn, colour=None, time_class=None, time_control=None, opening=None):
    conditions = []
    params = []
    if colour is not None:
        conditions.append('my_colour = ?')
        params.append(colour)
    if time_class is not None:
        conditions.append('time_class = ?')
        params.append(time_class)
    if time_control is not None:
        conditions.append('time_control = ?')
        params.append(time_control)
    if opening is not None:
        conditions.append('opening LIKE ?')
        params.append(f'%{opening}%')
    where = ''
    if conditions:
        where = 'WHERE ' + ' AND '.join(conditions)

    return conn.execute(f'''
        SELECT COUNT(*),
               SUM(my_result = 'win'),
               SUM(my_result = 'loss'),
               SUM(my_result = 'draw')
        FROM games
        {where}
    ''', params).fetchone()