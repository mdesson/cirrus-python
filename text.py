from sys import exit
from flask import Flask, request as REQUEST, redirect
from twilio.twiml.messaging_response import MessagingResponse
from weather import *
from scheduler import scheduler

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def cirrus():
    """Texts weather dependent on user input."""
    body = REQUEST.values.get('Body', None)
    resp = MessagingResponse()

    if body.lower() == 'c' or body.lower() == 'current':
        resp.message(current_weather())

    elif body.lower() == 'd' or body.lower() == 'day':
        weather = generate_hours()
        hourly_report = ['HOURLY REPORT:']
        for i in weather:
            hourly_report.append(repr(i))

        if len('\n\n'.join(hourly_report))+38 < 1600: # 38 characters to offset "Sent from your Twilio trial account - "
            resp.message('\n\n'.join(hourly_report))
        else:
            part_one = '\n\n'.join(hourly_report[0:int(len(hourly_report) / 2 + 1)])
            part_two = '\n\n'.join(hourly_report[int(len(hourly_report) / 2 + 1):int(len(hourly_report) - 1)])
            resp.message(part_one)
            resp.message(part_two)

    elif body.lower() == 'w' or body.lower() == 'week':
        weather = generate_weekdays()
        weekly_report = ['THIS WEEK:']
        for i in weather:
            weekly_report.append(repr(i))
        resp.message('\n\n'.join(weekly_report))

    elif body.lower() == 'e' or body.lower() == 'exit':
        resp.message("Ending program. Goodbye1")
        exit()

    else:
        resp.message(
            '\nTo get the weather:\n1) Send \'c\' or \'current\' to get the current weather.\n2) Send \'d\' or \'day\' '
            'to get the next 24 hours.\n3) Send \'w\' or \'week\' to get the next seven days.\n4) \'e\' or \'exit\' to '
            'exit.)

    return str(resp)


if __name__ == '__main__':
    current_weather()
    app.run(debug=True)
