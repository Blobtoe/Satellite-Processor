import logging
from bottle import Bottle, ServerAdapter, WSGIRefServer, post, run, request, response, get
from threading import Thread, Event
import json
from datetime import datetime

# local imports
from PassPredictor import PassPredictor
import utils

class WSGIServer(ServerAdapter):
    '''
    custom ServerAdapter to allow for a shutdown method (credit: https://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop)
    '''
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

class Webserver(Thread):
    '''
    provides an API for the scheduler
    '''
    def __init__(self, predictor, scheduler):
        Thread.__init__(self)
        
        # set exit event for when we want to stop
        self.exit_event = Event()

        # get the predictor for the specified satellites
        self.predictor = predictor

        # get the scheduler
        self.scheduler = scheduler

        # start the custom WSGI server
        self.server = WSGIServer(host="localhost", port=utils.get_config()["webserver_port"])

        # start the thread
        self.start()
    
    # GET /status
    def status(self):
        logging.info(f"Serving /status to {request.remote_addr}")

        # return the scheduler's status
        return json.dumps(self.scheduler.status)

    # POST /future_passes (satellites [, start_date=now, pass_count=1, min_elevation=0, max_elevation=90, min_sun_elevation=-90, max_sun_elevation=90]
    def future_passes(self):
        logging.info(f"Serving /future_passes to {request.remote_addr}")

        # get the request parameters
        parameters = request.json
        keys = list(parameters.keys())

        # if the satellites parameter is missing, return an error
        if "satellites" not in keys:
            response.status == 400
            return "not all required parameters given"
        else:
            # parse request parameters
            start_date = parameters["start_date"] if "start_date" in keys else datetime.now()
            pass_count = parameters["pass_count"] if "pass_count" in keys else 1
            satellites = [utils.get_satellite(name) for name in parameters["satellites"]]
            min_elevation = parameters["min_elevation"] if "min_elevation" in keys else 0
            max_elevation = parameters["max_elevation"] if "max_elevation" in keys else 90
            min_sun_elevation = parameters["min_sun_elevation"] if "min_sun_elevation" in keys else -90
            max_sun_elevation = parameters["max_sun_elevation"] if "max_sun_elevation" in keys else 90

            # create predictor for specified satellites
            predictor = PassPredictor(start_date, None, satellites, min_elevation, max_elevation, min_sun_elevation, max_sun_elevation)
            
            # return the number of passes requested
            return json.dumps([next(predictor).json() for i in range(pass_count)])

    def exit(self):
        '''
        stop the webserver
        '''
        logging.info("Stopping webserver")

        # stop the WSGI server
        self.server.stop()

        # set the exit event
        self.exit_event.set()

        # join thread
        self.join()
        logging.info("done")

    def run(self):
        '''
        start the webserver
        '''
        app = Bottle()

        # add routes
        app.route("/status", method="GET", callback=self.status)
        app.route("/future_passes", method="POST", callback=self.future_passes)

        # run the server
        run(app=app, server=self.server, debug=False, quiet=True)