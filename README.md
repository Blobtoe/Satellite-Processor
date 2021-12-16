<h1 align="center"> Satellite Processor </h1>

### **Current Work in Progress**

Satellite Processor is automatic satellite prediction and processing software. It is meant to be run on a central processing server in parallel with recording nodes running <a href="https://github.com/Blobtoe/Satellite-Recorder">Satellite Recorder</a>. It is build completely with Python, but uses external command line tools to do the processing. When a satellite is overhead, the server will ask a node to start recording. The node will then pipe I/Q data to the server for processing.

## Features
- Configurable satellites and downlinks
- Web API to access status, future passes, or old passes from other applications
- Simultaneous processing (work in progress)

## Installing
```
# clone this repo
git clone https://github.com/Blobtoe/Satellite-Processor.git
cd Satellite-Processor
# assign execution permissions
chmod +x SatelliteProcessor.py
# run Satellite Processor
./SatelliteProcessor.py
```

## Upcoming Features
- Actually processing lol

## External Tools
- <a href="https://wxtoimgrestored.xyz/">**wxtoimg**</a> for APT decoding
- **wxmap** for APT overlays and projections
- <a href="https://github.com/dbdexter-dev/meteor_demod">**meteor_demod**</a> for LRPT demodulation
- <a href="https://github.com/altillimity/SatDump">**satdump**</a> for LRPT overlays and projections