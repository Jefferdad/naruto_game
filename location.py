import json
import sqlite3

def get_location(id):

    ret = None
    with open("data/location_map.json", "r") as f:
        jsontext = f.read()
        d = json.loads(jsontext)
        d['id'] = id
        ret = Location(**d)

class Location():

    def __init__(self, id=0, name="A Room", description="An empty room", neighbors={}):
        self.id = id
        self.name = name
        self.description = description
        self.neighbors = neighbors
        
    def _neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None
        
    def north(self):
        return self._neighbor('n')
    
    def south(self):
        return self._neighbor('s')
        
    def east(self):
        return self._neighbor('e')
        
    def west(self):
        return self._neighbor('w')