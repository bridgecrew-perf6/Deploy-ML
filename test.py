import requests


resp = requests.post("http://127.0.0.1:5000", json={'hasil': 2})
#resp = requests.post("http://127.0.0.1:5000", files={'file': open('eight.png', 'rb')})

print(resp.json())