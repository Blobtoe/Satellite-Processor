import logging
from threading import Thread, Event
from datetime import datetime
from time import sleep

class PassScheduler(Thread):
    '''
    schedules processing of satellite passes
    '''
    def __init__(self, predictor):
        Thread.__init__(self)
        
        # set exit event for when we want to stop
        self.exit_event = Event()

        # get the predictor for the specified satellites
        self.predictor = predictor

        # set status
        self.status = {"status": "starting"}

        # start the thread
        self.start()
    
    def exit(self):
        '''
        stops the scheduler
        '''
        logging.info("Stopping scheduler")

        # set the exit event
        self.exit_event.set()

        # join thread
        self.join()
        logging.info("done")

    def run(self):
        '''
        main scheduler loop
        '''
        logging.info("Starting scheduler")

        # get first pass from the predictor
        next_pass = next(self.predictor)

        # set status
        logging.info(f"Waiting for {next_pass}")
        self.status = {"status": f"Waiting for {next_pass}"}

        # loop until scheduler is stopped
        while not self.exit_event.is_set():
            # wait until the next pass's start time
            if datetime.now() > next_pass.aos:
                # process the pass
                next_pass.process()

                #get the next pass from the predictor
                next_pass = next(self.predictor)

                # set status
                logging.info(f"Waiting for {next_pass}")
                self.status = {"status": f"Waiting for {next_pass}"}
            sleep(0.1)
            
