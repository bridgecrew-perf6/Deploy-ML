import requests


resp = requests.post("https://capstone-lxoqzmsemq-et.a.run.app", json={'hasil': 2})
#resp = requests.post("http://127.0.0.1:5000", files={'file': open('eight.png', 'rb')})

print(resp.json())