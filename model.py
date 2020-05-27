#!bin/python3.8

import json
from math import pi

class Agent:
    def __init__(self, position, **agent_attributes):
        self.position = position
        for attr_name, attr_value in agent_attributes.items():
            setattr(self, attr_name, attr_value)

class Position:

    def __init__(self, longitude_degrees, latitude_degrees):
        self.longitude_degrees = longitude_degrees
        self.latitude_degrees = latitude_degrees

    @property
    def longitude(self):
        return self.longitude_degrees * pi / 180

    @property
    def latitude(self):
        # Latitude in radians
        return self.latitude_degrees * pi / 180
        
class Zone:

    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    WIDTH_DEGREES = 1 #DEGREES OF LONGITUDE
    HEIGHT_DEGREES = 1 #degrees of latiude

    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1 # degrees of longitude
    HEIGHT_DEGREES = 1 # degrees of latitude

    ZONES = []
    @classmethod
    def initialize_zones(cls):
        for latitude in range (cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)
        print(len(cls.ZONES))

    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self.inhabitants = []

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)
    
    @property
    def population(self):
        return len(self.inhabitants)

    def contains(self, position):
        return position.longitude >= min(self.corner1.longitude, self.corner2.longitude) and \
            position.longitude < max(self.corner1.longitude, self.corner2.longitude) and \
            position.latitude >= min(self.corner1.latitude, self.corner2.latitude) and \
            position.latitude < max(self.corner1.latitude, self.corner2.latitude)
            
    @classmethod
    def find_zone_that_contains(cls, position):
        # Compute the index in the ZONES array that contains the given position
        longitude_index = int((position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES)/ cls.WIDTH_DEGREES)
        latitude_index = int((position.latitude_degrees - cls.MIN_LATITUDE_DEGREES)/ cls.HEIGHT_DEGREES)
        longitude_bins = int((cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES) # 180-(-180) / 1
        zone_index = latitude_index * longitude_bins + longitude_index

        # Just checking that the index is correct
        zone = cls.ZONES[zone_index]
        assert zone.contains(position)

        return zone
        
    EARTH_RADIUS_KILOMETERS = 6371

    @property
    def width(self):
        return (self.corner1.longitude - self.corner2.longitude) * self.EARTH_RADIUS_KILOMETERS
    
    @property
    def height(self):
        return abs(self.corner1.latitude - self.corner2.latitude) * self.EARTH_RADIUS_KILOMETERS
    
    @property
    def area(self):
        return self.height * self.width

    def population_density(self):
        return self.population / self.area

    def average_agreeableness(self):
        if not self.inhabitants:
            return 0
        return sum([inhabitant.agreeableness for inhabitant in self.inhabitants]) / self.population

def main():
    Zone.initialize_zones()
    for agent_attributes in json.load(open("agents-100k.json")):
        latitude_degrees = agent_attributes.pop("latitude")
        longitude_degrees = agent_attributes.pop("longitude")
        position = Position(longitude_degrees, latitude_degrees)
        agent = Agent(position, **agent_attributes)
        zone = Zone.find_zone_that_contains(position)
        zone.add_inhabitant(agent)
        print(zone.width)
#first_agent = Agent(**agent_attributes)
print("ok")
main()