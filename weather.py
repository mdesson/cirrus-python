from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

week_req = request.Request("https://weather.gc.ca/city/pages/qc-147_metric_e.html", headers=headers)
# hour_req = request.Request("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html", headers=headers)

res = request.urlopen(week_req)
html = res.read()
soup = BeautifulSoup(html, "lxml")

spans = soup.find_all("span", {'class': "wxo-metric-hide"})

values = []

for span in spans:
    values.append(span.get_text())

print(values)
# DESIGN #
# Find !!! in soup.txt. id = "mainContent"
# For weekly, use text descriptions lower on page
# 1st span is always current temp
