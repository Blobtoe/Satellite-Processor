from Downlink import Downlink
import logging
import os
from datetime import timedelta

import utils

class APT(Downlink):
    def process(self, sat_pass):
        logging.info(f"Processing APT")

        os.system(f"wxmap -T \"{sat_pass.satellite.name}\" -H \"{utils.get_config()['tle_location']}\" -p 0 -l 0 -g 0 -o \"{(sat_pass.aos + timedelta(seconds=90)).strftime('%d %b %Y %H:%M:%S')}\" \"{sat_pass.filename_base}.map.png\"")

        for tag in utils.get_config()["downlinks"]["APT"]["image_tags"]:
            if tag == "contrast_a":
                os.system(f"wxtoimg -m {sat_pass.filename_base}.map.png -A -i JPEG -a -e contrast {sat_pass.filename_base}.wav {sat_pass.filename_base}.{tag}.jpg")
            elif tag == "contrast_b":
                os.system(f"wxtoimg -m {sat_pass.filename_base}.map.png -A -i JPEG -b -e contrast {sat_pass.filename_base}.wav {sat_pass.filename_base}.{tag}.jpg")
            elif tag == "raw":
                os.system(f"wxtoimg -m {sat_pass.filename_base}.map.png -A -i JPEG {sat_pass.filename_base}.wav {sat_pass.filename_base}.{tag}.jpg")
            else:
                os.system(f"wxtoimg -m {sat_pass.filename_base}.map.png -A -i JPEG -e {tag} {sat_pass.filename_base}.wav {sat_pass.filename_base}.{tag}.jpg")