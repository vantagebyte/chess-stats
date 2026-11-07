from dataclasses import dataclass
from datetime import datetime, timezone

DRAW_RESULTS = ['agreed', 'repetition', 'stalemate', 'insufficient', '50move', 'timevsinsufficient']

@dataclass
class Game:
    url: str
    time_class: str
    time_control: str
    my_colour: str
    my_rating: int
    opponent_rating: int
    my_result: str
    start_time: int
    end_time: int
    opening: str

def clean_opening(name):
    words = name.split()
    kept = []
    for word in words:
        if word[0].isdigit() and '.' in word:
            break
        else:
            kept.append(word)
    return ' '.join(kept)

def get_start_time(pgn):
    lines = pgn.split('\n')
    for line in lines:
        if line.startswith('[UTCDate'):
            date = line.split('"')[1]
        elif line.startswith('[UTCTime'):
            time = line.split('"')[1]
    text = f'{date} {time}'
    start = datetime.strptime(text, '%Y.%m.%d %H:%M:%S')
    start = start.replace(tzinfo=timezone.utc)
    return int(start.timestamp())        


def parse_game(game, username):
    if game['white']['username'].lower() == username.lower():
        my_colour = 'white'
        me = game['white']
        opponent = game['black']
    else:
        my_colour = 'black'
        me = game['black']
        opponent = game['white']

    if me['result'] == 'win':
        my_result = 'win'
    elif me['result'] in DRAW_RESULTS:
        my_result = 'draw'
    else:
        my_result = 'loss'

    opening = clean_opening(game.get('eco','').split('/')[-1].replace('-',' '))
    return Game(
        url=game['url'],
        time_class=game['time_class'],
        time_control=game['time_control'],
        start_time=get_start_time(game['pgn']),
        end_time=game['end_time'],
        my_colour=my_colour,
        my_result=my_result,
        my_rating=me['rating'],
        opponent_rating=opponent['rating'],
        opening=opening
    )
