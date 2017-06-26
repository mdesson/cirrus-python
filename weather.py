from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)

class WeekDay:
    """WeekDay object contains weather data for a given day of the week.
    TEMP placeholder will show when no data was scraped for that attribute."""
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

    def __repr__(self):
        brief = [self.date.upper()]

        if self.high != "TEMP":
            brief.append("{} high".format(self.high))
        if self.low != "TEMP":
            brief.append("{} low".format(self.low))
        if self.condition_day != "TEMP":
            brief.append("Day: {}".format(self.condition_day))
        if self.PoP_day != "" and self.PoP_day != "TEMP":
            brief.append("{} chance of precipitation".format(self.PoP_day))
        if self.condition_night != "TEMP":
            brief.append("Night: {}".format(self.condition_night))
        if self.PoP_night != "" and self.PoP_night != "TEMP":
            brief.append("{} chance of precipitation".format(self.PoP_night))

        return '\n'.join(brief)


class Hour:
    """Hour object contains weather data for a hour in the next 24 hours.
    TEMP placeholder will show when no data was scraped for that attribute."""
    def __init__(self, time="TEMP", temp="TEMP", condition="TEMP", LoP="TEMP", wind="TEMP", gust="TEMP"):
        self.time = time
        self.temp = temp
        self.condition = condition
        self.LoP = LoP
        self.wind = wind
        self.gust = gust

    def __repr__(self):
        if self.gust != "":
            hour = "{}: {}°C. {} LoP. {}. Wind at {} km/h, gusts {} km/h.".format(self.time, self.temp, self.LoP,
                                                                                  self.condition, self.wind, self.gust)
        else:
            hour = "{}: {}°C. {} LoP. {}. Wind at {} km/h.".format(self.time, self.temp, self.LoP, self.condition,
                                                                   self.wind)

        return hour


def make_soup(url):
    """Generates soup object with given url."""
    res = request.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, "lxml")
    return soup


def class_weatherlist(tag, webclass, url):
    """Input a tag and webclass from the url's source to output a scraped list of of matching elements."""
    search = make_soup(url).find_all(tag, {"class": webclass})
    values = [x.get_text().replace('\n','') for x in search]
    return values


def header_weatherlist(tag, header, url):
    """Input a tag and header from the url's source to output a scraped list of of matching elements."""
    search = make_soup(url).find_all(tag, {"headers": header})
    values = [x.get_text().replace('\n','') for x in search]
    return values


# For debug purposes to get all element in webclass
def print_tag_list(existing_weatherlist):
    """Prints all elements for given class_weatherlist or header_weatherlist with index number.
    Mostly used for debug and building purposes."""
    x = 0
    for i in existing_weatherlist:
        print(str(x) + ' ' + i)
        x += 1


def generate_weekdays():
    """Generates a list of weekday objects for the next seven days."""
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
    """Generates a list of hour objects for the next 24 hours."""
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


def current_weather():
    """Returns a string describing the current weather."""
    current = class_weatherlist("dd", "mrgn-bttm-0", week_req)

    conditions = current[2].lower()
    tendency = current[5].lower()
    temp = current[6]
    wind = current[11]
    humidity = current[10]

    return "It is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}.".format(conditions,temp, tendency, wind, humidity)


if __name__ == "__main__":
    weekdays = generate_weekdays()
    hours = generate_hours()

    print("CURRENT WEATHER")
    current_weather()

    print("\nHOURLY REPORT")
    for i in hours:
        print(i)
        print("")

    print("WEEKDAY VERBOSE")
    for i in weekdays:
        print(i.verbose_weather(i.date, i.day, i.night))
        print("")

    print("WEEKDAY BRIEF")
    for i in weekdays:
        print(i)
        print("")
