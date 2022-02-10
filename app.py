import requests

headers = {"Referer": "https://www.betexplorer.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
s = requests.Session()
session = s.headers.update(headers)

request = s.get('https://www.sisal.it/api-betting/vrol-api/vrol/palinsesto/getAlberaturaEventiSingoli/1')
response = request.json()

print(response)

print('ale')
