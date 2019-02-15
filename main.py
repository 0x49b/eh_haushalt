#!/usr/bin/env python


from signal import SIGINT, SIGTERM, signal
from time import sleep
from Webserver import Webserver
import RPi.GPIO as GPIO


def main():

    global web

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    signal(SIGINT, exit_gracefully)
    signal(SIGTERM, exit_gracefully)

    web = Webserver.Webserver()
    web.start()

    while True:
        print "Iterate"
        sleep(5)


def exit_gracefully(signum, frame):

    web.stop()


main()
