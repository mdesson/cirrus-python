from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)


def make_soup(url):
    res = request.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, "lxml")
    return soup


class WeekDay:
    def __init__(self, date="TEMP", day="TEMP", night="TEMP", high="TEMP", low="TEMP", PoP_day="TEMP", PoP_night="TEMP", condition_day="TEMP", condition_night = "TEMP"):
        self.date = date
        self.day = day
        self.night = night
        self.high = high
        self.low = low
        self.PoP_day = PoP_day
        self.PoP_night = PoP_night
        self.condition_day = condition_day
        self.condition_night = condition_night

    def print_verbose(self, day, night):
        print("Placeholder")

    def print_brief(self, date, high, PoP, condition_day):
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
def weatherlist(tag, webclass, url):
    search = make_soup(url).find_all(tag, {"class": webclass})
    values = [x.get_text().replace('\n','') for x in search]
    return values


# For debug purposes to get all element in webclass. ==> REWRITE
def print_tag_list(existing_weatherlist):
    x = 0
    for i in existing_weatherlist:
        print(str(x) + ' ' + i)
        x += 1


def current_weather():
    current = weatherlist("dd", "mrgn-bttm-0", week_req)

    conditions = current[2].lower()
    tendency = current[5].lower()
    temp = current[6]
    wind = current[11]
    humidity = current[10]

    print("It is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}."
          .format(conditions, temp, tendency, wind, humidity))


def generate_weekdays():
    raw_dates = weatherlist("td", "uniform_width", week_req)
    raw_days = weatherlist("tr", "pdg-btm-0", week_req)
    raw_nights = weatherlist("tr", "pdg-tp-0", week_req)
    raw_brief = weatherlist('p', 'mrgn-bttm-0', week_req)
    weekdays = []

    date = WeekDay(date="Today", night=raw_nights[0].replace('Tonight', '').strip())
    del raw_nights[0]
    weekdays.append(date)

    # Create today weekday object
    if "Today" in raw_days[0]:
        weekdays[0].day = raw_days[0].replace('Today', '').strip()
        del raw_days[0]

    # Add day attribute
    for i in raw_dates:
        if i.strip() != "Night":
            date = WeekDay(date=i.strip())
            weekdays.append(date)

    # Add night attribute
    x = 0
    for i in weekdays[1:]:
        i.day = raw_days[x].replace(i.date, '').strip()
        try:
            i.night = raw_nights[x].replace('Night', '').strip()
        except:
            i.night = ''
        x += 1

    # Get brief weather during daytime
    if len(raw_brief) == 39:
        weekdays[0].high = raw_brief[0].strip().split("C",1)[0]+"C"
        weekdays[0].PoP_day = raw_brief[1].strip()
        weekdays[0].condition_day = raw_brief[2].strip()
        weekdays[0].low = raw_brief[21].strip().split("C",1)[0]+"C"
        weekdays[0].PoP_night = raw_brief[22].strip()
        weekdays[0].condition_night = raw_brief[23].strip()
        del raw_brief[0:3]
        del raw_brief[21:24]

        for i in range(1, 7):
            weekdays[i].high = raw_brief[0].strip().split("C",1)[0]+"C"
            del raw_brief[0]
            weekdays[i].PoP_day = raw_brief[0].strip()
            del raw_brief[0]
            weekdays[i].condition_day = raw_brief[0].strip()
            del raw_brief[0]

        for i in range(1, 6):
            weekdays[i].low = raw_brief[0].strip().split("C",1)[0]+"C"
            del raw_brief[0]
            weekdays[i].PoP_night = raw_brief[0].strip()
            del raw_brief[0]
            weekdays[i].condition_night = raw_brief[0].strip()
            del raw_brief[0]

    # get brief weather during night
    elif len(raw_brief) == 36:
        weekdays[0].low = raw_brief[18].strip().split("C",1)[0]+"C"
        weekdays[0].PoP_night = raw_brief[19].strip()
        weekdays[0].condition_night = raw_brief[20].strip()
        del raw_brief[18:21]

        for i in range(1, 7):
            weekdays[i].high = raw_brief[0].strip().split("C",1)[0]+"C"
            del raw_brief[0]
            weekdays[i].PoP_day = raw_brief[0].strip()
            del raw_brief[0]
            weekdays[i].condition_day = raw_brief[0].strip()
            del raw_brief[0]

        for i in range(1, 6):
            weekdays[i].low = raw_brief[0].strip().split("C",1)[0]+"C"
            del raw_brief[0]
            weekdays[i].PoP_night = raw_brief[0].strip()
            del raw_brief[0]
            weekdays[i].condition_night = raw_brief[0].strip()
            del raw_brief[0]

    return weekdays


def generate_hours():
    pass


current_weather()

weekdays = generate_weekdays()

print("DAY INFO:")
for i in weekdays:
    print(i.date, '\n', i.high, '\n', i.PoP_day, '\n', i.condition_day)

print("NIGHT INFO:")
for i in weekdays:
    print(i.date, ':\n', i.low, '\n', i.PoP_night, '\n', i.condition_night)

# NOTE: For hourly, learn to contend with time rolling over into next day
# BUGS:
# none :)
