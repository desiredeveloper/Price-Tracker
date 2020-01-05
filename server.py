#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import logging
import sys
import requests
from functools import wraps
import numpy as np
from flask import Flask, Response, jsonify, request
from flask_mail import Mail, Message
from scraper import Scraper

parser = argparse.ArgumentParser()

parser.add_argument(
    "--host", default="0.0.0.0", help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port", default=8500, help="The port of the server(eg. 8500)", type=int)
parser.add_argument(
    "--debug",
    default=False,
    help="Enable debug for flask or not(eg. False)",
    type=bool)

application = Flask(__name__)
application.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'it1402713094@gmail.com',
	MAIL_PASSWORD = 'yourpassword'
	)
mail = Mail(application)

def send_mail(msg):
	try:
		msgObj = Message("Send Mail Tutorial!",
		  sender="it1402713094@gmail.com",
		  recipients=["recievingemail@email.com"])
		msgObj.body = msg
		mail.send(msgObj)
	except Exception as e:
		return(str(e)) 


@application.route("/", methods=["POST"])
def subscribe():
    requestData = request.json
    product = Scraper(requestData.url,requestData.email)
    msgId = product.tracker()


def main():
    args = parser.parse_args(sys.argv[1:])
    application.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()