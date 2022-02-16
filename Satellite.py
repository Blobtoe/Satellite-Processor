from datetime import datetime
import predict

# local imports
import utils
from SatPass import SatPass

class Satellite:
    '''
    stores information about a satellite
    '''
    def __init__(self, name, downlinks):
        self.name = name
        self.tle = utils.get_tle(name)
        self.downlinks = downlinks

    def json(self) -> dict:
        return {
            "name": self.name,
            "downlinks": [downlink.json() for downlink in self.downlinks]
        }

class SatellitePredictor:
    '''
    predicts future passes for a satellites
    '''
    def __init__(self, satellite, start_date=datetime.now(), end_date=None, min_elevation=0, max_elevation=90, min_sun_elevation=-90, max_sun_elevation=90):
        self.start_date = start_date
        self.end_date = end_date
        self.min_elevation = min_elevation
        self.max_elevation = max_elevation
        self.min_sun_elevation = min_sun_elevation
        self.max_sun_elevation = max_sun_elevation
        self.groundstation_location = (utils.get_secrets()["lat"], -utils.get_secrets()["lon"], utils.get_secrets()["elev"])
        self.value = None
        self.satellite = satellite

        # create a predictor for the satellite
        self.predictor = predict.transits(satellite.tle, self.groundstation_location, ending_after=start_date.timestamp(), ending_before=end_date.timestamp() if end_date != None else None)

    def __iter__(self):
        return self

    def __next__(self):
        temp = next(self.predictor)
        sun_elevation = utils.get_sun_elevation(datetime.fromtimestamp(round(temp.peak()["epoch"])))
        
        # loop until we find a pass that meets the criteria
        while datetime.fromtimestamp(round(temp.start)) < self.start_date or \
            (datetime.fromtimestamp(round(temp.start)) > self.end_date if self.end_date != None else False) or \
            temp.peak()["elevation"] < self.min_elevation or \
            temp.peak()["elevation"] > self.max_elevation or \
            sun_elevation < self.min_sun_elevation or \
            sun_elevation > self.max_sun_elevation:
            temp = next(self.predictor)
        
        # create a pass object
        self.value = SatPass(self.satellite, datetime.fromtimestamp(round(temp.start)), datetime.fromtimestamp(round(temp.peak()["epoch"])), datetime.fromtimestamp(round(temp.end)), round(temp.peak()["elevation"], 1), round(temp.duration()), round(temp.at(temp.start)["azimuth"], 1), round(temp.at(temp.end)["azimuth"], 1), sun_elevation)
        
        # return the pass object
        return self.value