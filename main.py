import re
import json
import requests 
from datetime import date,datetime,timedelta
from bs4 import BeautifulSoup 


class track:
    def __init__(self,url):
        self.URL = url

    # def pidExists(pid):


    def tracker(self):
        r = requests.get(self.URL) 
        soup = BeautifulSoup(r.content, 'html5lib')

        pid = re.findall("(?<=pid=)(.*?&)",self.URL)[0][:-1]

        price = soup.find('div', attrs = {'class':'_1vC4OE _3qQ9m1'}).text
        price = re.sub("[\D]","",price)

        today = date.today()
        yesterday = str(today-timedelta(days=1))
        str_today = str(today)

        with open('tracker.json', 'r') as f:
            trackData = json.load(f)
            
            if trackData.get(pid) is None:
                trackData[pid] = {}

            x = datetime.now().hour
            if(trackData[pid][str_today] is None):
                trackData[pid][str_today] = [{"min":str(float("inf"))}]

            trackData[pid][str_today].append({x:price})

            trackData[pid][str_today][0]['min'] = min(trackData[pid][str_today][0]['min'], price)

            
            # if(trackData[pid][yesterday]["min"] > trackData[pid][str_today]["min"]):
            #     print('Price down!')

        with open('tracker.json', 'w', encoding='utf-8') as f:
            json.dump(trackData, f, ensure_ascii=False, indent=4)

product = track("https://www.flipkart.com/microsoft-kw900140-windows-10-home-oem-dvd-64-bit/p/itmemdh72fh4cxp5?pid=OPSEMDH6NY8AHUTF&lid=LSTOPSEMDH6NY8AHUTFHLGWQF&marketplace=FLIPKART&fm=productRecommendation%2FcrossSelling&iid=R%3Ac%3Bp%3ACOMFHKKHVGHUBYHW%3Bl%3ALSTCOMFHKKHVGHUBYHWZINLQQ%3Bpt%3App%3Buid%3A7d5c521d-d2f3-de6f-02ac-31ebe24f03b5%3B.OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF&ppt=ProductPage&ppn=ProductPage&ssid=t19lcptf7vfwq3gg1577699839675&otracker=pp_reco_Bought%2BTogether_40_33.productCard.PMU_TAB_Microsoft%2BKW900140%2BWindows%2B10%2BHome%2BOem%2BDVD%2B64%2Bbit_OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF_productRecommendation%2FcrossSelling_0&otracker1=pp_reco_PINNED_productRecommendation%2FcrossSelling_Bought%2BTogether_GRID_productCard_cc_40_NA_view-all&cid=OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF")

product.tracker()