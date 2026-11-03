import requests

HEADERS = {'User-Agent': 'chess-stats/1.0 (github.com/vantagebyte)'}

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