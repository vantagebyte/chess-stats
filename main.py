import requests
from dataclasses import dataclass

HEADERS = {'User-Agent': 'chess-stats/1.0 (github.com/vantagebyte)'}
DRAW_RESULTS = ['agreed', 'repetition', 'stalemate', 'insufficient', '50move', 'timevsinsufficient']

@dataclass
class Game:
    url: str
    time_class: str
    my_colour: str
    my_rating: int
    opponent_rating: int
    my_result: str
    end_time: int
    opening: str


def get_archives(username):

    url = f'https://api.chess.com/pub/player/{username}/games/archives'

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        archives = data['archives']
        return archives
    else:
        print(f'Error: {response.status_code}')
        return []

def get_games(month_url):

    response = requests.get(month_url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        games = data['games']
        return games
    else:
        print(f'Error: {response.status_code}')
        return []

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

    opening = game.get('eco','').split('/')[-1].replace('-',' ')
    return Game(
        url=game['url'],
        time_class=game['time_class'],
        end_time=game['end_time'],
        my_colour=my_colour,
        my_result=my_result,
        my_rating=me['rating'],
        opponent_rating=opponent['rating'],
        opening=opening
    )

username = 'Voolfenborg'
archives = get_archives(username)
last_month = archives[-2]
games = get_games(last_month)
print(len(games))

blitz_count = 0
for game in games:
    if game['time_class'] == 'blitz':
        blitz_count += 1
print(blitz_count)


print(games[0]['eco'])
print(parse_game(games[0],username))
