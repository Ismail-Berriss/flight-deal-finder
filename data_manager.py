import requests
import config

sheety_prices_endpoint = config.SHEETY_PRICES_ENDPOINT
sheety_users_endpoint = config.SHEETY_USERS_ENDPOINT
sheety_headers = {
    "Authorization": config.SHEETY_TOKEN,
}


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_prices_endpoint, headers=sheety_headers)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_data(self):
        for row in self.destination_data:
            body = {
                "price": {
                    "iataCode": row["iataCode"]
                },
            }
            response = requests.put(url=f"{sheety_prices_endpoint}/{row["id"]}", json=body, headers=sheety_headers)
            response.raise_for_status()

    def get_users(self):
        response = requests.get(url=sheety_users_endpoint, headers=sheety_headers)
        self.customer_data = response.json()["users"]
        return self.customer_data
