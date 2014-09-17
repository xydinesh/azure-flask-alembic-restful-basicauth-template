import requests
import json

def signup():
    r = requests.post('http://localhost:5555/api/signup', data=json.dumps({'username': 'dinesh', 'password':'python'}), headers={'Content-Type': 'application/json'})
    print r.text

def get_token():
    r = requests.post('http://localhost:5555/api/token', auth=('dinesh', 'python'))
    return (json.loads(r.text))['token']

if __name__ == '__main__':
    token = get_token()
    r = requests.get('http://localhost:5555/api/greeting', auth=(token, ''))
    print r.text