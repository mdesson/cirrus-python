import os
import datetime
import time
from weather import generate_hours
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
to_phone = os.environ['PERSONAL_PHONE_NUMBER']
from_phone = os.environ['TWILIO_PHONE_NUMBER']

client = Client(account_sid, auth_token)


def send_message(body):
    """ Sends text message using argument as body."""
    client.messages.create(
        to=to_phone,
        from_=from_phone,
        body=body
    )


def morning_message():
    """Sends next 24h of weather for Montreal. To be sent by scheduler() every morning at 7:00am."""
    weather = generate_hours()
    hourly_report = ['HOURLY REPORT:']
    for i in weather:
        hourly_report.append(repr(i))

    if len('\n\n'.join(hourly_report)) + 38 < 1600:  # 38 characters to offset "Sent from your Twilio trial account - "
        send_message('\n\n'.join(hourly_report))
    else:
        part_one = '\n\n'.join(hourly_report[0:int(len(hourly_report) / 2 + 1)])
        part_two = '\n\n'.join(hourly_report[int(len(hourly_report) / 2 + 1):int(len(hourly_report) - 1)])
        send_message(part_one)
        send_message(part_two)


def get_next_7am():
    """Determines (roughly) the total number seconds until it will next be 7:00am."""
    now = datetime.datetime.now()
    if now.minute != 0:
        hour = 24 - datetime.datetime.now().hour + 6  # returns int of hours until 6th hour
        minute = now.minute
        second = now.second
        countdown = datetime.timedelta(hours=hour, minutes=minute, seconds=second).total_seconds()
        return int(countdown)
    else:
        hour = 24 - now.hour + 7  # returns int of hours until 7th hour
        minute = now.minute
        second = now.second
        countdown = datetime.timedelta(hours=hour, minutes=minute, seconds=second).total_seconds()
        return int(countdown)


def scheduler():
    """Sends a text when it is next 7:00am, and loops until main loop in text.py is broken."""
    for i in range(get_next_7am()):  # Increments by 1s to make keyboard interrupt possible.
        time.sleep(1)
    morning_message()

    while True:
        time.sleep(86400)  # Number of seconds in 24 hours
        morning_message()


if __name__ == '__main__':
    get_next_7am()
    scheduler()
