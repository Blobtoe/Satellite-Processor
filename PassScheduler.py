import logging
from threading import Thread, Event
from datetime import datetime
from time import sleep

class PassScheduler(Thread):
    def __init__(self, predictor):
        Thread.__init__(self)
        self.exit_event = Event()
        self.predictor = predictor
        self.status = {"status": "starting"}
        self.start()
    
    def exit(self):
        self.exit_event.set()
        self.join()

    def run(self):
        logging.info("Starting scheduler")
        next_pass = next(self.predictor)
        logging.info(f"Waiting for {next_pass}")
        self.status = {"status": f"Waiting for {next_pass}"}
        while not self.exit_event.is_set():
            if datetime.now() > next_pass.aos:
                next_pass.process()
                next_pass = next(self.predictor)
                logging.info(f"Waiting for {next_pass}")
                self.status = {"status": f"Waiting for {next_pass}"}
            sleep(0.1)
            
