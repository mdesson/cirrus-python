from bs4 import BeautifulSoup
from urllib import request

now_week = request.urlopen("https://weather.gc.ca/city/pages/qc-147_metric_e.html")
hourly = request.urlopen("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html")

soup = BeautifulSoup(now_week, "lxml")

with open("soup.txt", 'w') as file:
    file.write(soup.prettify())

# Now + Weekly: https://weather.gc.ca/city/pages/qc-147_metric_e.html
# Hourly: https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html
