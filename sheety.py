import requests
import config

sheety_endpoint = config.SHEETY_USERS_ENDPOINT
sheety_headers = {
    "Authorization": config.SHEETY_TOKEN,
}


def post_new_row(first_name, last_name, email):
    new_user = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }
    response = requests.post(url=sheety_endpoint, json=new_user, headers=sheety_headers)
    print(response.json())


