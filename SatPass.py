import logging

import utils

class SatPass:
    '''
    stores information about a satellite pass
    '''
    def __init__(self, satellite, aos, tca, los, peak_elevation, duration, aos_azimuth, los_azimuth, sun_elevation):
        self.satellite = satellite
        self.aos = aos
        self.tca = tca
        self.los = los
        self.peak_elevation = peak_elevation
        self.duration = duration
        self.aos_azimuth = aos_azimuth
        self.los_azimuth = los_azimuth
        self.sun_elevation = sun_elevation
        self.output_dir = f"{utils.get_config()['output_dir']}/{aos.strftime('%Y')}/{aos.strftime('%Y-%m')}/{aos.strftime('%Y-%m-%d')}/{aos.strftime('%Y-%m-%d_%H.%M.%S')}"
        self.filename_base = f"{self.aos.strftime('%Y-%m-%d_%H.%M.%S')}"

    def json(self) -> dict:
        return {
            "satellite": self.satellite.json(),
            "aos": self.aos.timestamp(), 
            "tca": self.tca.timestamp(), 
            "los": self.los.timestamp(), 
            "peak_elevation": self.peak_elevation, 
            "duration": self.duration, 
            "aos_azimuth": self.aos_azimuth, 
            "los_azimuth": self.los_azimuth,
            "sun_elevation": self.sun_elevation
        }

    def __repr__(self) -> str:
        return f"{self.peak_elevation} deg {self.satellite.name} pass at {self.aos}"
    
    def process(self):
        '''
        process the satellite pass
        '''
        logging.info(f"Processing {self}")
        self.satellite.downlinks[0].process(self)