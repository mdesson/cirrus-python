from bs4 import BeautifulSoup
from urllib import request

now_week = request.urlopen("https://weather.gc.ca/city/pages/qc-147_metric_e.html")
hourly = request.urlopen("https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html")

soup = BeautifulSoup(now_week, "lxml")

soup.prettify()

# Now + Weekly: https://weather.gc.ca/city/pages/qc-147_metric_e.html
# Hourly: https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html

# NOW SECTION:
# <div class="col-sm-2 brdr-rght  text-center" style="vertical-align: top; min-height: 166px;"><img width="60" height="51" class="center-block mrgn-tp-md" src="/weathericons/12.gif" alt="Light Rain" title="Light Rain"><p class="visible-xs text-center">Light Rain</p>
#             <div>
#               <p class="text-center mrgn-tp-md mrgn-bttm-sm lead"><span class="wxo-metric-hide">7°<abbr title="Celsius">C</abbr>
#                 </span><span class="wxo-imperial-hide wxo-city-hidden">45°<abbr title="Fahrenheit">F</abbr>
#                 </span>
#               </p>
#               <ul class="list-inline list-unstyled text-center wxo-imperial-hide wxo-city-hidden hidden-print">
#                 <li>
#                   <a class="wxo-btn-metric-toggle" href="/city/pages/qc-147_metric_e.html" title="Convert to Metric Units">°C</a>
#                 </li>
#                 <li class="brdr-lft">°<abbr title="Fahrenheit">F</abbr>
#                 </li>
#               </ul>
#               <ul class="list-inline list-unstyled text-center wxo-metric-hide hidden-print">
#                 <li>°<abbr title="Celsius">C</abbr>
#                 </li>
#                 <li class="brdr-lft">
#                   <a class="wxo-btn-imperial-toggle" href="qc-147_metric_e.html?unit=imperial" data-link-id="qc-147_metric_e.html?unit=imperial" title="Convert to Imperial Units">°F
#                         </a>
#                 </li>
#               </ul>
#             </div>
#           </div>