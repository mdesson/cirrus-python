# Cirrus
Delivering you the weather via text from the Internet to your phone.

## Using Cirrus
To use Cirrus simply text any of the following case-insensitive options:

1) "d" or "day": This outputs today's weather for the next 24 hours.

2) "w" or "week": This outputs the next seven days of weather.

3) "c" or "current": This outputs The current weather.

Any other input will result in a message explaining the above options.

## Scraping the Weather
Using BeautifulSoup4, Cirrus scrapes data from the following two URLs:

https://weather.gc.ca/city/pages/qc-147_metric_e.html

https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html

The output is a list of objects for each URL. The first one is the next seven days of weather, the second one is the next 24 hours of weather.

There is also a function which outputs a string with the current weather.

It would be possible to use any Environment Canada page to output the weather for any Canadian city.
## Text Messaging the Weather
Cirrus uses Twilio with Flask to output the weather. String length is within the 1600 character limit, even if the user is on a Twilio trial account.

Note that to make this work I used ngrok to connect to Twilio.

## About Cirrus
This is my first real project, and was borne out of a desire for a simple weather app which delivers reliable weather reports.