from datetime import datetime
from Satellite import SatellitePredictor

class PassPredictor:
    def __init__(self, start_date=datetime.now(), end_date=None, satellites=None, min_elevation=0, max_elevation=90, min_sun_elevation=-90, max_sun_elevation=90):
        self.start_date = start_date
        self.end_date = end_date
        self.satellites = satellites
        self.min_elevation = min_elevation
        self.max_elevation = max_elevation
        self.min_sun_elevation = min_sun_elevation
        self.max_sun_elevation = max_sun_elevation
        self.value = None
        self.predictors = [SatellitePredictor(satellite, self.start_date, self.end_date, self.min_elevation, self.max_elevation, self.min_sun_elevation, self.max_sun_elevation) for satellite in self.satellites]

    def __iter__(self):
        return self

    def __next__(self):
        next_predictor = None
        for predictor in self.predictors:
            if predictor.value == None:
                next(predictor)
            if next_predictor == None:
                next_predictor = predictor
            elif predictor.value.aos < next_predictor.value.aos:
                next_predictor = predictor
        next_pass = next_predictor.value
        next(next_predictor)
        self.value = next_pass
        return next_pass

            




