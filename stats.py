def results_summary(conn):
    return conn.execute('SELECT my_result, COUNT(*) FROM games GROUP BY my_result').fetchall()
