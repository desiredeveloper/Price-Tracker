import re
import json

class Subscriber:
    def __init__(self,url,email,threshold):
        self.URL = url
        self.email = email
        self.threshold = threshold


    def subscribe(self):
        try:
            if(re.match("^(http:\/\/|https:\/\/)",self.URL)):
                pid = re.findall("(?<=pid=)(.*?&)",self.URL)[0][:-1]
            else:
                return "URL should start with http or https"
        except Exception as e:
            return "Please enter a valid Flipkart URL"

        with open('tracker.json', 'r') as f:
            trackData = json.load(f)
            
            if trackData.get(pid) is None:
                trackData[pid] = {}
                trackData[pid]['mailing_list'] = []
                trackData[pid]['global_min'] = self.threshold if self.threshold else str(float("inf"))
                trackData[pid]['URL'] = self.URL

            trackData[pid]['mailing_list'].append(self.email)

        with open('tracker.json', 'w', encoding='utf-8') as f:
            json.dump(trackData, f, ensure_ascii=False, indent=4)
        

# product = Subscriber("https://www.flipkart.com/microsoft-kw900140-windows-10-home-oem-dvd-64-bit/p/itmemdh72fh4cxp5?pid=OPSEMDH6NY8AHUTF&lid=LSTOPSEMDH6NY8AHUTFHLGWQF&marketplace=FLIPKART&fm=productRecommendation%2FcrossSelling&iid=R%3Ac%3Bp%3ACOMFHKKHVGHUBYHW%3Bl%3ALSTCOMFHKKHVGHUBYHWZINLQQ%3Bpt%3App%3Buid%3A7d5c521d-d2f3-de6f-02ac-31ebe24f03b5%3B.OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF&ppt=ProductPage&ppn=ProductPage&ssid=t19lcptf7vfwq3gg1577699839675&otracker=pp_reco_Bought%2BTogether_40_33.productCard.PMU_TAB_Microsoft%2BKW900140%2BWindows%2B10%2BHome%2BOem%2BDVD%2B64%2Bbit_OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF_productRecommendation%2FcrossSelling_0&otracker1=pp_reco_PINNED_productRecommendation%2FcrossSelling_Bought%2BTogether_GRID_productCard_cc_40_NA_view-all&cid=OPSEMDH6NY8AHUTF.LSTOPSEMDH6NY8AHUTFHLGWQF",
#             'it1@toy.com')

# product.subscribe()