import smtplib as sl
import json
import re
import sys
import argparse
import urllib.request
import requests
import atexit
from bs4 import BeautifulSoup 
from datetime import date,datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

parser = argparse.ArgumentParser()

parser.add_argument(
	"--classId", default="_1vC4OE _3qQ9m1", help="Class for scrapping")
parser.add_argument(
	"--interval", 
	default=15, 
	help="Time interval between each notification(eg. 15)", 
	type=int)
args = parser.parse_args(sys.argv[1:])

cron = BlockingScheduler()

@cron.scheduled_job('interval',id='my_job_id',minutes=args.interval)
def send_mail():
	try:
		with urllib.request.urlopen("https://laptophunt.herokuapp.com/data") as url:
			r = requests.get(trackData[pid]['URL']) 

			trackData = json.loads(url.read().decode())

			today = date.today()
			yesterday = str(today-timedelta(days=1))
			str_today = str(today)

			for pid in trackData:
				msg = 0
				r = requests.get(trackData[pid]['URL']) 
				soup = BeautifulSoup(r.content, 'html5lib')

				price = soup.find('div', attrs = {'class':args.classId}).text
				price = re.sub("[\D]","",price)

				x = str(datetime.now())

				if trackData[pid].get(str_today) is None:
					trackData[pid][str_today] = [{"min":str(float("inf"))}]

				trackData[pid][str_today].append({x:price})

				trackData[pid][str_today][0]['min'] = min(trackData[pid][str_today][0]['min'], price)

				# if(trackData[pid][yesterday][0]["min"] > trackData[pid][str_today][0]["min"]):
				# 	msg = "Better price than yesterday for \n" + trackData[pid]['URL']+ " The price now is Rs."+price

				if trackData[pid]['global_min']>price:
					trackData[pid]['global_min'] = price
					msg = "Lowest Price ever for \n"+ trackData[pid]['URL'] +"\n\n Available @ Rs."+ price

				if msg!=0:
					recv_list = trackData[pid]['mailing_list']
					import smtplib as sl
					server = sl.SMTP('smtp.gmail.com', 587)
					server.ehlo()
					server.starttls()
					server.ehlo()
					server.login('it1402713094@gmail.com','flaskapp')
					message = 'Subject: {}\n\n{}'.format("Update on product-ID : "+pid, msg)
					server.sendmail('it1402713094@gmail.com',recv_list,message)
				requests.post("https://laptophunt.herokuapp.com/setdata", data = trackData)
                    
	except Exception as e:
		print(str(e))

cron.start()
# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
