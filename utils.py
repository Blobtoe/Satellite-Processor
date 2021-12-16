from datetime import datetime
import requests
from PIL import Image
from pathlib import Path
import json
import ephem
import enum
import logging

from Satellite import Satellite
from Downlink import Downlink
from APT import APT
from LRPT import LRPT

local_path = Path(__file__).parent

last_tle_update = None

def get_config():
    '''returns the json data in the config file'''

    with open(local_path / "config.json") as f:
        return json.load(f)


def get_secrets():
    '''returns the json data in the secrets file'''

    with open(local_path / "secrets.json") as f:
        return json.load(f)

def download_tle():
    '''
    download the "active" tle file from celestrak
    '''

    logging.info("Downloading TLE file")
    # make the request to the website
    r = requests.get("https://www.celestrak.com/NORAD/elements/active.txt")
    # save the response to a file
    tle_file = get_config()["tle_location"]
    open(tle_file, "w+").write(r.text.replace("\r", ""))


def get_tle(satellite_name):
    '''
    returns the parsed tle lines from the tle file
    '''
    global last_tle_update

    # if the tle is out of date
    if last_tle_update == None or (datetime.now() - last_tle_update).total_seconds() / 3600 >= get_config()["tle_update_frequency"]:
        download_tle()
        last_tle_update = datetime.now()

    tle_file = get_config()["tle_location"]
    # pad the satellite name with spaces to make it 24 characters long
    satellite_name = satellite_name.ljust(24, " ")
    # read the lines of the tle file
    with open(tle_file, "r") as f:
        lines = f.read().splitlines()
    # get the index of the satellite's name
    index = lines.index(satellite_name)
    # return the 3 lines at the index
    return "\n".join(lines[index:index+3])

def get_satellites() -> list:
    config = get_config()
    satellites = []
    for satellite in config["satellites"]:
        downlinks = []
        for downlink in config["satellites"][satellite]["downlinks"].keys():
            parameters = config["satellites"][satellite]["downlinks"][downlink]
            downlinks.append(Downlinks[downlink].value(parameters["frequency"], parameters["bandwidth"], parameters["min_elevation"], parameters["priority"], downlink))
        satellites.append(Satellite(satellite, downlinks))
    return satellites

def get_satellite(satellite_name) -> Satellite:
    try:
        satellite_config = get_config()["satellites"][satellite_name]
        downlinks = [Downlinks[downlink].value(satellite_config["downlinks"][downlink]["frequency"], satellite_config["downlinks"][downlink]["bandwidth"], satellite_config["downlinks"][downlink]["min_elevation"], satellite_config["downlinks"][downlink]["priority"], downlink) for downlink in satellite_config["downlinks"]]
        return Satellite(satellite_name, downlinks)
    except:
        logging.error(f"Failed to get satellite \"{satellite_name}\"")
        return None

def get_sun_elevation(time):
    # compute the sun elevation at peak elevation
    # start ephem for sun elevation predictions
    obs = ephem.Observer()
    obs.lat = str(get_secrets()["lat"])
    obs.long = str(get_secrets()["lon"])
    obs.date = time
    sun = ephem.Sun(obs)
    sun.compute(obs)
    return round(float(sun.alt) * 57.2957795, 1)  # convert from radians to degrees
    
class Downlinks(enum.Enum):
    APT = APT
    LRPT = LRPT
