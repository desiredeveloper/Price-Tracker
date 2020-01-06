#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import sys
import re
import requests
from flask import Flask, request
from flask_mail import Mail, Message
from subscriber import Subscriber
import atexit
from bs4 import BeautifulSoup 
from datetime import date,datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

parser = argparse.ArgumentParser()

parser.add_argument(
    "--host", default="0.0.0.0", help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port", default=8500, help="The port of the server(eg. 8500)", type=int)
parser.add_argument(
	"--classId", default="_1vC4OE _3qQ9m1", help="Class for scrapping")
parser.add_argument(
    "--debug",
    default=False,
    help="Enable debug for flask or not(eg. False)",
    type=bool)
parser.add_argument(
	"--interval", 
	default=60, 
	help="Time interval between each notification(eg. 15)", 
	type=int)

args = parser.parse_args(sys.argv[1:])
application = Flask(__name__)
application.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'it1402713094@gmail.com',
	MAIL_PASSWORD = 'flaskapp'
	)
mail = Mail(application)


cron = BlockingScheduler()
cron.start()

@cron.scheduled_job('interval',id='my_job_id',minutes=args.interval)
def send_mail():
	try:
		with open('tracker.json', 'r') as f:
			trackData = json.load(f)

			today = date.today()
			yesterday = str(today-timedelta(days=1))
			str_today = str(today)

			for pid in trackData:
				msg = 0
				r = requests.get(trackData[pid]['URL']) 
				soup = BeautifulSoup(r.content, 'html5lib')

				price = soup.find('div', attrs = {'class':args.classId}).text
				price = re.sub("[\D]","",price)

				x = datetime.now()

				if trackData[pid].get(str_today) is None:
					trackData[pid][str_today] = [{"min":str(float("inf"))}]

				trackData[pid][str_today].append({x:price})

				trackData[pid][str_today][0]['min'] = min(trackData[pid][str_today][0]['min'], price)

				if(trackData[pid][yesterday][0]["min"] > trackData[pid][str_today][0]["min"]):
					msg = "Better price than yesterday for \n" + trackData[pid]['URL']+ " The price now is Rs."+price

				if trackData[pid]['global_min']>price:
					trackData[pid]['global_min'] = price
					msg = "Lowest Price ever for \n"+ trackData[pid]['URL'] +"\n\n Available @ Rs."+ price
				
				if msg!=0:
					recv_list = trackData[pid]['mailing_list']
					msgObj = Message("Update on product-ID :"+pid,
					sender="it1402713094@gmail.com",
					recipients= recv_list)
					msgObj.body = msg
					mail.send(msgObj)
	except Exception as e:
		return(str(e))

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))


@application.route("/", methods=["POST"])
def subscriber():
    requestData = request.json
    product = Subscriber(requestData.url,requestData.email)
    product.subscribe()

def main():
    application.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()