from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)

res = request.urlopen(week_req)
html = res.read()
soup = BeautifulSoup(html, "lxml")


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


current_weather = weatherlist("dd", "mrgn-bttm-0")

conditions = current_weather[2].lower()
tendency = current_weather[5].lower()
temp = current_weather[6]
wind = current_weather[11]
humidity = current_weather[10]


print("It is {} outside. The temperature is {} and {}. The wind is {} and humidity is at {}."
      .format(conditions, temp, tendency, wind, humidity))

# DESIGN #
# Find !!! in soup.txt. id = "mainContent"
# For verbose weekly, use text descriptions lower on page
# For brief weekly, use chart below current chart
