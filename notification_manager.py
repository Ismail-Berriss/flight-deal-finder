from twilio.rest import Client
import smtplib
import config


class NotificationManager:

    def __init__(self):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    def send_notification(self, message):
        sms_message = self.client.messages \
            .create(
                body=message,
                from_=config.TWILIO_PHONE_N,
                to=config.MY_PHONE_N,
            )
        print(sms_message.status)

    def send_emails(self, users, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(config.MY_EMAIL, config.MY_PASSWORD)
            for user in users:
                connection.sendmail(
                    from_addr=config.MY_EMAIL,
                    to_addrs=user["email"],
                    msg=f"Subject:Dear {user["lastName"]} {user["firstName"]}\n\n{message}".encode("utf-8")
                )

