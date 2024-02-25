from pprint import pprint
import datetime as dt

import sheety
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LON"


if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()

tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_month_from_today = dt.datetime.now() + dt.timedelta(days=6*30)

for row in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        row["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        flight = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            row["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            stop_overs=1
        )
        pprint(flight)
        if flight is None:
            continue

    notification_manager = NotificationManager()

    if flight.price < row["lowestPrice"]:
        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop overs, via {flight.via_city}"

    # pprint(data_manager.get_users())
        notification_manager.send_emails(users=data_manager.get_users(), message=message)

# import sheety
#
# print("Welcome to Ismail's Flight Club.\nWe find the best flight deals and email you.")
# first_name = input("What is your first name?\n")
# last_name = input("What is your last name?\n")
#
# correct = False
# while not correct:
#     email = input("What is your email?\n")
#     email_again = input("Type your email again.\n")
#     if email == email_again:
#         correct = True
#         sheety.post_new_row(first_name, last_name, email)
#         print("You're in the club!")
#     else:
#         print("The email do not match! Try again.")
