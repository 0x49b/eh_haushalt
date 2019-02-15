#!/usr/bin/env python


from signal import SIGINT, SIGTERM, signal
from time import sleep
from Webserver import Webserver
import RPi.GPIO as GPIO
import json


def main():

    global web, id, data, stats

    id = 10
    data = json.loads("""
    [{
		"id": 11,
		"status": "on",
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
		"status": "on",
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
        "points": 0
    }
    """)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    signal(SIGINT, exit_gracefully)
    signal(SIGTERM, exit_gracefully)

    web = Webserver.Webserver(10, data, stats)
    web.start()

    while True:
        print "Iterate"
        sleep(5)


def exit_gracefully(signum, frame):

    web.stop()


main()
