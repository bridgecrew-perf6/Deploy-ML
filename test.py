import requests


resp = requests.post("https://capstone-lxoqzmsemq-et.a.run.app", files={'file': open('14_1_2_20170104012048369.jpg.chip.jpg', 'rb')})
#resp = requests.post("http://127.0.0.1:5000", files={'file': open('eight.png', 'rb')})

print(resp.json())