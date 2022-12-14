import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('API_KEY')
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

def main():
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={API_KEY}"
    data = {"email": EMAIL, "password": PASSWORD, "returnSecureToken": True}

    result = requests.post(url=uri, data=data)

    user = result.json()

    print(user['idToken'])


if __name__ == '__main__':
    main()
