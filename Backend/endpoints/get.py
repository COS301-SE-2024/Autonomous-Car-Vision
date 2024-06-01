import requests
import base64

user_id = 5

url = 'http://127.0.0.1:8000/api/users/'
url = f'{url}{user_id}/'
username = 'donatellogc'
password = 'password'

credentials = f'{username}:{password}'
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_credentials}'
}

response = requests.get(url, headers=headers)
print(response.json())