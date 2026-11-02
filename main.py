import requests

def get_archives(username):

    url = f'https://api.chess.com/pub/player/{username}/games/archives'

    headers = {'User-Agent': 'chess-stats/1.0 (github.com/vantagebyte)'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        archives = data['archives']
        return archives
    for month_url in archives:
        print(month_url)
    else:
        print(f'Error: {response.status_code}')
        return []

username = 'Voolfenborg'
archives = get_archives(username)
for month_url in archives:
    print(month_url)


