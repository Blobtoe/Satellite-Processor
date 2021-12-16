import logging
from time import sleep

import utils
from PassPredictor import PassPredictor
from PassScheduler import PassScheduler
from WebServer import Webserver

def main():
    logging.info("Starting Satellite Processor")
    predictor = PassPredictor(satellites=utils.get_satellites(), min_elevation=20)
    scheduler = PassScheduler(predictor)
    webserver = Webserver(predictor, scheduler)

    logging.info("Press CTRL+C to stop")
    try:
        while True:
            sleep(5)
    finally:
        webserver.exit()
        scheduler.exit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    main()