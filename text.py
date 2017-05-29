from flask import Flask, request as REQUEST, redirect
from twilio.twiml.messaging_response import MessagingResponse
from weather import *

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    '''Send a dynamic reply to an incoming text message'''
    # Get the message the user sent our Twilio number
    body = REQUEST.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body.lower() == 'c' or body.lower() == 'current':
        resp.message(current_weather())
    elif body.lower() == 'd' or body.lower() == 'day':
        weather = generate_hours()
        hourly_report = ['HOURLY REPORT:']
        for i in weather:
            hourly_report.append(i.print_hour(i.time, i.temp, i.condition, i.LoP, i.wind, i.gust))
        resp.message('\n\n'.join(hourly_report))
    elif body.lower() == 'w' or body.lower() == 'week':
        weather = generate_weekdays()
        weekly_report = ['THIS WEEK:']
        for i in weather:
            weekly_report.append(i.print_brief(i.date, i.high, i.low, i.PoP_day, i.PoP_night, i.condition_day, i.condition_night))
        resp.message('\n\n'.join(weekly_report))
    else:
        resp.message(
            '\nTo get the weather:\n1) Send \'c\' or \'current\' to get the current weather.\n2) Send \'d\' or \'day\' '
            'to get the next 24 hours.\n3) Send \'w\' or \'week\' to get the next seven days.')

    return str(resp)

if __name__ == '__main__':
    current_weather()
    app.run(debug=True)
