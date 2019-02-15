#!/usr/bin/env python


from signal import SIGINT, SIGTERM, signal
from time import sleep
from Webserver import Webserver


def main():

    global web

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
