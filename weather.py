from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)

res = request.urlopen(week_req)
html = res.read()
soup = BeautifulSoup(html, "lxml")


class WeekDay:
    def __init__(self, date, high, PoP, condition, day, night):
        self.date = date
        self.high = high
        self.PoP = PoP
        self.condition = condition
        self.day = day
        self.night = night

    def print_weekday(self, date, high, PoP, condition):
        print("Placeholder")

    def print_verbose(self, day, night):
        print("Placeholder")


class Hour:
    def __init__(self, time, temp, condition, LoP, wind, humidex):
        self.time = time
        self.temp = temp
        self.condition = condition
        self.LoP = LoP
        self.wind = wind
        self.humidex = humidex

    def print_hour(self, time, temp, condition, LoP, wind, humidex):
        print("Placeholder")


# returns list of elements with given tag and class
def weatherlist(tag, webclass):
    search = soup.find_all(tag, {"class": webclass})
    values = [x.get_text().replace('\n','') for x in search]
    return values


# For debug purposes to get all element in webclass.
def print_tag_list(existing_weatherlist):
    x = 0
    for i in existing_weatherlist:
        print(str(x) + ' ' + i)
        x +=1


def print_current():
    current_weather = weatherlist("dd", "mrgn-bttm-0")

    conditions = current_weather[2].lower()
    tendency = current_weather[5].lower()
    temp = current_weather[6]
    wind = current_weather[11]
    humidity = current_weather[10]

    print("It is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}."
          .format(conditions, temp, tendency, wind, humidity))


def generate_weekdays():
    print("Code goes here")
    return weekdays

print("DAY inc. DATE:")
print_tag_list(weatherlist("tr", "pdg-btm-0"))
print("\nDATE Only:")
print_tag_list(weatherlist("td", "uniform_width"))
print("\nNIGHT inc. DATE:")
print_tag_list(weatherlist("tr", "pdg-tp-0")) # Special case for "Tonight"
print("\nCURRENT:")
print_current()

# NOTE: For hourly, learn to contend with time rolling over into next day
