#!/usr/bin/env python3

import logging
from time import sleep
import signal

# local imports
import utils
from PassPredictor import PassPredictor
from PassScheduler import PassScheduler
from WebServer import Webserver


def stop(webserver, scheduler):
    '''
    stop the scheduler and webserver
    '''
    print()
    logging.info("Stopping Satellite Processor")

    # stop the webserver
    webserver.exit()

    # stop the scheduler
    scheduler.exit()

    # exit
    exit(0)

def main():
    '''
    start the scheduler and webserver
    '''
    logging.info("Starting Satellite Processor")

    # get a PassPredictor for the specified satellites
    predictor = PassPredictor(satellites=utils.get_satellites(), min_elevation=20)

    # start the scheduler
    scheduler = PassScheduler(predictor)

    # start the webserver
    webserver = Webserver(predictor, scheduler)

    # pause until the user wants to stop
    logging.info("Press CTRL+C to stop")
    signal.signal(signal.SIGINT, lambda sig, frame: stop(webserver, scheduler))
    signal.pause()
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    main()