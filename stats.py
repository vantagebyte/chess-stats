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
    