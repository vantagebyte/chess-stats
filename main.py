import requests

username = 'Voolfenborg'

url = f'https://api.chess.com/pub/player/{username}/games/archives'

headers = {'User-Agent': 'chess-stats/1.0 (github.com/vantagebyte)'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('Connected')
    data = response.json()
    archives = data['archives']
    for month_url in archives:
        print(month_url)
else:
    print(f'Error: {response.status_code}')

