class Downlink:
    def __init__(self, frequency, bandwidth, min_elevation, priority, name):
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.min_elevation = min_elevation
        self.priority = priority
        self.name = name
    
    def json(self) -> dict:
        return {
            "frequency": self.frequency,
            "bandwidth": self.bandwidth,
            "min_elevation": self.min_elevation,
            "priority": self.priority,
            "name": self.name
        }
