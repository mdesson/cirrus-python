from flask import Flask, request as REQUEST, redirect
from twilio.twiml.messaging_response import MessagingResponse
from weather import *

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
        resp.message('\n\n'.join(hourly_report))

        if len('\n\n'.join(hourly_report)) < 1600:
            return '\n\n'.join(hourly_report)
        else:
            if len(hourly_report) % 2 == 0:
                part_one = '\n\n'.join(hourly_report[0:int(len(hourly_report)/2-0.5)])
                part_two = '\n\n'.join(hourly_report[int(len(hourly_report)/2+0.5):int(len(hourly_report)-1)])
                resp.message(part_one)
                resp.message(part_two)
            else:
                part_one = '\n\n'.join(hourly_report[0:len(hourly_report)/2])
                part_two = '\n\n'.join(hourly_report[len(hourly_report)/2+1:len(hourly_report)-1])
                resp.message(part_one)
                resp.message(part_two)

    elif body.lower() == 'w' or body.lower() == 'week':
        weather = generate_weekdays()
        weekly_report = ['THIS WEEK:']
        for i in weather:
            weekly_report.append(repr(i))
        resp.message('\n\n'.join(weekly_report))

    else:
        resp.message(
            '\nTo get the weather:\n1) Send \'c\' or \'current\' to get the current weather.\n2) Send \'d\' or \'day\' '
            'to get the next 24 hours.\n3) Send \'w\' or \'week\' to get the next seven days.')


if __name__ == '__main__':
    current_weather()
    app.run(debug=True)
