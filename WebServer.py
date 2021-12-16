from bottle import post, run, request, response, get
from threading import Thread, Event
import json
from datetime import datetime

from PassPredictor import PassPredictor
import utils

class Webserver(Thread):
    def __init__(self, predictor, scheduler):
        Thread.__init__(self)
        self.exit_event = Event()
        self.predictor = predictor
        self.scheduler = scheduler
        self.start()
    
    # GET /status
    def status(self):
        return json.dumps(self.scheduler.status)

    # POST /future_passes (satellites [, start_date=now, pass_count=1, min_elevation=0, max_elevation=90, min_sun_elevation=-90, max_sun_elevation=90]
    def future_passes(self):
        parameters = request.json
        keys = list(parameters.keys())
        if "satellites" not in keys:
            response.status == 400
            return "not all required parameters given"
        else:
            start_date = parameters["start_date"] if "start_date" in keys else datetime.now()
            pass_count = parameters["pass_count"] if "pass_count" in keys else 1
            satellites = [utils.get_satellite(name) for name in parameters["satellites"]]
            min_elevation = parameters["min_elevation"] if "min_elevation" in keys else 0
            max_elevation = parameters["max_elevation"] if "max_elevation" in keys else 90
            min_sun_elevation = parameters["min_sun_elevation"] if "min_sun_elevation" in keys else -90
            max_sun_elevation = parameters["max_sun_elevation"] if "max_sun_elevation" in keys else 90
            predictor = PassPredictor(start_date, None, satellites, min_elevation, max_elevation, min_sun_elevation, max_sun_elevation)
            return json.dumps([next(predictor).json() for i in range(pass_count)])

    def exit(self):
        self.exit_event.set()
        self.join()

    def run(self):
        post("/future_passes")(self.future_passes)
        get("/status")(self.status)
        run(host="localhost", port=utils.get_config()["webserver_port"], debug=True, quiet=True)