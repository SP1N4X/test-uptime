import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept": "application/json, text/plain, */*",
    "DNT": "1", 
    "Connection": "keep-alive", 
    "Upgrade-Insecure-Requests": "1"
    }
response = requests.get('https://www.sisal.it/api-betting/vrol-api/vrol/palinsesto/getAlberaturaEventiSingoli/1', headers=headers)
print(response.json())
