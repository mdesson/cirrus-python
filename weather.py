from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)

res = request.urlopen(week_req)
html = res.read()
soup = BeautifulSoup(html, "lxml")


class WeekDay:
    def __init__(self, date="TEMP", high="TEMP", PoP="TEMP", condition="TEMP", day="TEMP", night="TEMP"):
        self.date = date
        self.day = day
        self.night = night
        self.high = high
        self.PoP = PoP
        self.condition = condition

    def print_verbose(self, day, night):
        print("Placeholder")

    def print_weekday(self, date, high, PoP, condition):
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


def current_weather():
    current = weatherlist("dd", "mrgn-bttm-0")

    conditions = current[2].lower()
    tendency = current[5].lower()
    temp = current[6]
    wind = current[11]
    humidity = current[10]

    print("It is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}."
          .format(conditions, temp, tendency, wind, humidity))


def generate_weekdays():
    raw_dates = weatherlist("td", "uniform_width")
    raw_days = weatherlist("tr", "pdg-btm-0")
    raw_nights = weatherlist("tr", "pdg-tp-0")
    weekdays = []

    date = WeekDay(date="Today", night=raw_nights[0].replace('Tonight', '').strip(), day='')
    del raw_nights[0]
    weekdays.append(date)

    if "Today" in raw_days[0]:
        weekdays[0].day = raw_days[0].replace('Today', '').strip()
        del raw_days[0]

    for i in raw_dates:
        if i.strip() != "Night":
            date = WeekDay(date=i.strip())
            weekdays.append(date)

    x = 0
    for i in weekdays[1:]:
        i.day = raw_days[x].replace(i.date, '').strip()
        try:
            i.night = raw_nights[x].replace('Night', '').strip()
        except:
            pass
        x += 1

    return weekdays

current_weather()

weekdays = generate_weekdays()

for i in weekdays:
    print(i.date, ':\n', i.day, '\n', i.night)

# NOTE: For hourly, learn to contend with time rolling over into next day
# BUGS:
# none :)
