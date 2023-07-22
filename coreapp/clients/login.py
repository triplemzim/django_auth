import requests

def client():
    data = {
        'username': 'regUser',
        'password': 'adminadmin',
    }

    response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data = data)

    print('Status code: ', response.status_code)
    response_data = response.json()
    
    print(response_data)


if __name__ == "__main__":
    client()