import requests

def client():
    data = {
        'username': 'regUser',
        'password1': 'adminadmin',
        'password2': 'adminadmin',
        'email': 'reguser@django.com'
    }

    response = requests.post("http://127.0.0.1:8000/api/rest-auth/registration/", data = data)

    print('Status code: ', response.status_code)

    print(response.json())


if __name__ == "__main__":
    client()