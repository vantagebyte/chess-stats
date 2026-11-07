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

def format_hour(hour):
    h = int(hour)
    if h == 0:
        return '12am'
    elif h < 12:
        return f'{h}am'
    elif h == 12:
        return '12pm'
    else:
        return f'{h % 12}pm'

def print_row(label, total, wins, losses, draws, width):
    if total == 0:
        print(f'{label:<{width}}   no games')
        return
    win_pct = wins / total * 100
    loss_pct = losses / total * 100
    draw_pct = draws / total * 100
    print(f'{label:<{width}} {total:>4} games | {win_pct:5.1f}% W | {loss_pct:5.1f}% L | {draw_pct:4.1f}% D')

def print_filtered(label, row):
    total, wins, losses, draws = row
    print_row(label, total, wins, losses, draws, len(label))
