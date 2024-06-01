import requests
import base64

url = 'http://127.0.0.1:8000/api/users/'
username = 'donatellogc'
password = 'password'

credentials = f'{username}:{password}'
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_credentials}'
}

data = {
    'uname': 'test',
    'uemail': 'test@gmail.com'
}

response = requests.post(url, headers=headers, json=data)
print(response.json())