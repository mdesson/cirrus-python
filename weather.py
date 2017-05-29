from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)


class WeekDay:
    def __init__(self, date="TEMP", day="TEMP", night="TEMP", high="TEMP", low="TEMP", PoP_day="TEMP", PoP_night="TEMP",
                 condition_day="TEMP", condition_night="TEMP"):
        self.date = date
        self.day = day
        self.night = night
        self.high = high
        self.low = low
        self.PoP_day = PoP_day
        self.PoP_night = PoP_night
        self.condition_day = condition_day
        self.condition_night = condition_night

    def print_verbose(self, date, day, night):
        print(date.upper())
        if day != "TEMP" and night != "":
            print("Day: {}".format(day))
            print("Night: {}".format(night))
        elif day != "TEMP":
            print("Day: {}".format(day))
        elif night != "":
            print("Night: {}".format(night))
        else:
            print("Error! No weather data for given date.")

    def print_brief(self, date, high, low, PoP_day, PoP_night, condition_day, condition_night):
        print(date.upper())

        if high != "TEMP":
            print("{} high".format(high))
        if low != "TEMP":
            print("{} low".format(low))
        if condition_day != "TEMP":
            print("Day: {}".format(condition_day))
        if PoP_day != "" and PoP_day != "TEMP":
            print("{} chance of precipitation".format(PoP_day))
        if condition_night != "TEMP":
            print("Night: {}".format(condition_night))
        if PoP_night != "" and PoP_night != "TEMP":
            print("{} chance of precipitation")


class Hour:
    def __init__(self, time="TEMP", temp="TEMP", condition="TEMP", LoP="TEMP", wind="TEMP", gust="TEMP"):
        self.time = time
        self.temp = temp
        self.condition = condition
        self.LoP = LoP
        self.wind = wind
        self.gust = gust

    def print_hour(self, time, temp, LoP, condition, wind, gust):
        if gust != "":
            print("{}: {}°C. {}. {} chance of precipitation. Wind at {} km/h, with gusts of {} km/h."
                  .format(time, temp, LoP, condition, wind, gust))
        else:
            print("{}: {}°C. {}. {} chance of precipitation. Wind at {} km/h."
                  .format(time, temp, LoP, condition, wind))


def make_soup(url):
    res = request.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, "lxml")
    return soup


# returns list of elements with given tag and class
def class_weatherlist(tag, webclass, url):
    search = make_soup(url).find_all(tag, {"class": webclass})
    values = [x.get_text().replace('\n','') for x in search]
    return values


def header_weatherlist(tag, header, url):
    search = make_soup(url).find_all(tag, {"headers": header})
    values = [x.get_text().replace('\n','') for x in search]
    return values


# For debug purposes to get all element in webclass. ==> REWRITE
def print_tag_list(existing_weatherlist):
    x = 0
    for i in existing_weatherlist:
        print(str(x) + ' ' + i)
        x += 1


def current_weather():
    current = class_weatherlist("dd", "mrgn-bttm-0", week_req)

    conditions = current[2].lower()
    tendency = current[5].lower()
    temp = current[6]
    wind = current[11]
    humidity = current[10]

    return str("\nIt is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}."
          .format(conditions, temp, tendency, wind, humidity))


def generate_weekdays():
    raw_dates = class_weatherlist("td", "uniform_width", week_req)
    raw_days = class_weatherlist("tr", "pdg-btm-0", week_req)
    raw_nights = class_weatherlist("tr", "pdg-tp-0", week_req)
    raw_brief = class_weatherlist('p', 'mrgn-bttm-0', week_req)
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
    raw_times = header_weatherlist("td", "header1", hour_req)
    raw_temps = header_weatherlist("td", "header2", hour_req)
    raw_conds = header_weatherlist("td", "header3", hour_req)
    raw_LoP = header_weatherlist("td", "header4", hour_req)
    raw_wind = []
    raw_gust = []
    hours_list = []

    for i in header_weatherlist("td", "header5", hour_req): # .split() it to get individual stuff
        x = i.split()
        raw_wind.append(x[1])
        try:
            raw_gust.append(x[3])
        except IndexError:
            raw_gust.append("")

    counter = 0
    for i in raw_LoP:
        if i == 'Nil':
            raw_LoP[counter] = "No"
            counter+= 1

    counter = 0
    for i in raw_times:
        hours_list.append(Hour(time=raw_times[counter], temp=raw_temps[counter], condition=raw_conds[counter],
                               LoP=raw_LoP[counter], wind=raw_wind[counter], gust=raw_gust[counter]))
        counter += 1

    return hours_list


if __name__ == "__main__":
    weekdays = generate_weekdays()
    hours = generate_hours()

    print("CURRENT WEATHER")
    current_weather()

    print("\nHOURLY REPORT")
    for i in hours:
        i.print_hour(i.time, i.temp, i.condition, i.LoP, i.wind, i.gust)
        print("")

    print("WEEKDAY VERBOSE")
    for i in weekdays:
        i.print_verbose(i.date, i.day, i.night)
        print("")

    print("WEEKDAY BRIEF")
    for i in weekdays:
        i.print_brief(i.date, i.high, i.low, i.PoP_day, i.PoP_night, i.condition_day, i.condition_night)
        print("")

# BUGS:
# none :)
