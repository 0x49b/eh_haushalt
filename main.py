#!/usr/bin/env python

from signal import SIGINT, SIGTERM, signal
from time import sleep
from Webserver import Webserver
import RPi.GPIO as GPIO
import json
import httplib2


def main():

    global web, id, data, stats, h

    h = httplib2.Http()

    id = 10
    data = json.loads("""
    [{
		"id": 11,
		"status": true,
		"name": "Freezer",
		"times": [{
			"startTime": "NULL",
			"endTime": "NULL",
			"minDuration": "NULL"
		}],
		"gpio": 18
	},
	{
		"id": 12,
		"status": true,
		"name": "Charging Station",
		"times": [{
			"startTime": "NULL",
			"endTime": "NULL",
			"minDuration": "NULL"
		}],
		"gpio": 23
	}]""")

    stats = json.loads("""
    {
      "customer": {
        "id": 10,
        "name": "Mike Mueller",
        "address": "Hilfikerstrasse 1",
        "zip": "3003",
        "location": "Bern",
        "points": 0
      }
    }
    """)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(18, True)
    GPIO.output(23, True)

    signal(SIGINT, exit_gracefully)
    signal(SIGTERM, exit_gracefully)

    (resp, content) = h.request("http://192.168.99.12:3000/assets?id=10", "POST", body=json.dumps(stats), headers={'content-type':'application/json'})

    stats = json.loads(content)

    web = Webserver.Webserver(10, data, stats)
    web.start()

    while True:
        update_status()
        sleep(5)


def update_status():
    global web
    status = web.get_stats()
    assets = web.get_assets()
    status['customer']['assets'] = assets
    (resp, content) = h.request("http://192.168.99.12:3000/assets?id=10", "PUT", body=json.dumps(status), headers={'content-type':'application/json'})

    newstatus = json.loads(content)
    web.set_assets(newstatus['customer']['assets'])
    del newstatus['customer']['assets']
    web.set_stats(newstatus)
    print content


def exit_gracefully(signum, frame):

    web.stop()


main()
