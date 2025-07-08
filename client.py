import requests

BASE = 'http://localhost:5000/'

request = requests.post(BASE + '/auth/login', {'username': 'pippo', 'password': 'poppo'})
response = request.json()
print(response)